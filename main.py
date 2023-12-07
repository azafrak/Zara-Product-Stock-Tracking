import json
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot

# JSON dosyalarından sabit bilgileri oku
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Sabit bilgileri güncelle
driver_path = config["driver_path"]
user_agent = config["user_agent"]
webdriver_wait_timeout = config["webdriver_wait_timeout"]
asyncio_sleep_duration = config["asyncio_sleep_duration"]
TELEGRAM_TOKEN = config["telegram_token"]
TELEGRAM_CHAT_ID = config["telegram_chat_id"]

# Chrome Options
chrome_options = Options()
for arg, value in config["chrome_options"].items():
    chrome_options.add_argument(f"--{arg}={value}")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--headless=new')

# Create Chrome service
chrome_service = ChromeService(executable_path=driver_path)

# Stok durumu bilgisini her bir ürün için sakla
previous_stock_status = {}

async def check_product(driver, product):
    url = product["url"]
    product_id = product["product_id"]
    item_id = product["item_id"]

    try:
        while True:
            # Ürün sayfasını aç
            driver.get(url)

            # Bekleme süresi için bir WebDriverWait oluştur
            wait = WebDriverWait(driver, 10)

            # Ürün sayfasındaki beden numarasını seçmeye çalış
            beden_element = wait.until(EC.element_to_be_clickable((By.ID, 'product-size-selector-{0}-item-{1}'.format(product_id, item_id))))
            beden_element.click()

            # Stok durumunu kontrol et
            stok_durumu_element = wait.until(
                EC.presence_of_element_located((By.ID, 'product-size-selector-{0}-item-{1}'.format(product_id, item_id))))
            stok_durumu = stok_durumu_element.get_attribute('data-qa-action')

            # Beden numarasını içeren elementi bul
            beden_numarasi_element = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'li#product-size-selector-{0}-item-{1} .product-size-info__main-label'.format(product_id, item_id))))
            beden_numarasi = beden_numarasi_element.text

            # Her bir ürün için ayrı stok durumu sakla
            if url not in previous_stock_status:
                previous_stock_status[url] = {'current': stok_durumu, 'previous': None}

            # Stok durumu değiştiğinde mesaj gönder
            if stok_durumu != previous_stock_status[url]['previous']:
                print_message = None
                if stok_durumu == 'size-in-stock':
                    print_message = 'Ürün stokta!'
                elif stok_durumu == 'size-low-on-stock':
                    print_message = 'Ürün az sayıda stokta!'
                elif stok_durumu == 'size-back-soon':
                    print_message = 'Ürün yakında gelecek!'
                elif stok_durumu == 'size-out-of-stock':
                    print_message = 'Ürün stokta değil!'

                if print_message:
                    bot = Bot(token=TELEGRAM_TOKEN)
                    message = f'🚨*Takip ettiğin {print_message}*\n\nBeden: {beden_numarasi}\nStok Durumu: {print_message}\nÜrün Linki: {url}'
                    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
                    previous_stock_status[url]['previous'] = stok_durumu

                    # Sonuçları ekrana yazdır
                    print(f'Seçilen beden numarası: {beden_numarasi}\n{print_message}')

            # Belirli bir süre bekleyerek tekrar kontrol etme
            await asyncio.sleep(10)  # Örnek olarak 10 saniye bekletme

            # Tarayıcıyı sürekli kapatıp açmak yerine mevcut açık olan sekmeyi yenileyip kontrolü sağla
            driver.refresh()

    except Exception as e:
        print(f'Hata: {str(e)}')

async def main():
    try:
        tasks = [check_product(webdriver.Chrome(service=chrome_service, options=chrome_options), product) for product in config["products"]]
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f'Hata: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
