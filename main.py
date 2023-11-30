import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot

# Telegram Bot Bilgileri
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''


async def main():
    try:
        # Set headless mode to new
        headless = True

        # Set the path to the ChromeDriver
        driver_path = "/Volumes/YEDEK/Masaüstü/Projelerim/Python_Proje/Urun_Stok_Takip/Zara Stok Bilgilendirme/chromedriver-mac-x64/chromedriver"

        # Set the path to the Google Chrome binary
        chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

        # User-Agent
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

        # Create Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new" if headless else "")
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={user_agent}")

        # Create Chrome service
        chrome_service = ChromeService(executable_path=driver_path)

        # Create Chrome driver
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        while True:
            # Ürün sayfasını aç
            url = 'https://www.zara.com/tr/tr/z1975-straight-high-waist-cropped-boncuklu-jean-p06147195.html'
            driver.get(url)

            # Bekleme süresi için bir WebDriverWait oluştur
            wait = WebDriverWait(driver, 10)

            # Ürün sayfasındaki beden numarasını seçmeye çalış
            beden_element = wait.until(EC.element_to_be_clickable((By.ID, 'product-size-selector-298629453-item-1')))
            beden_element.click()

            # Stok durumunu kontrol et
            stok_durumu_element = wait.until(
                EC.presence_of_element_located((By.ID, 'product-size-selector-298629453-item-1')))
            stok_durumu = stok_durumu_element.get_attribute('data-qa-action')

            # Beden numarasını içeren elementi bul
            beden_numarasi_element = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'li#product-size-selector-298629453-item-1 .product-size-info__main-label')))
            beden_numarasi = beden_numarasi_element.text

            # Sonuçları ekrana yazdır
            print(f'Seçilen beden numarası: {beden_numarasi}')

            # Telegram mesajını gönderme
            bot = Bot(token=TELEGRAM_TOKEN)

            if stok_durumu == 'size-in-stock':
                print_message = 'Ürün stokta!'
                message = f'🚨*Takip ettiğin ürün stoğa girdi. Acele Et!*🚨\n\nBeden: {beden_numarasi}\nStok Durumu: {print_message}\nÜrün Linki: {url}'
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
            elif stok_durumu == 'size-low-on-stock':
                print_message = 'Ürün az sayıda stokta!'
                message = f'🚨*Takip ettiğin ürün az sayıda stokta. Acele Et!*🚨\n\nBeden: {beden_numarasi}\nStok Durumu: {print_message}\nÜrün Linki: {url}'
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
            else:
                print_message = 'Ürün stokta değil!'
                message = f'Takip ettiğin ürün stokta değil. 😢\n\nBeden: {beden_numarasi}\nStok Durumu: {print_message}\nÜrün Linki: {url}'
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

            print(print_message)

            # Belirli bir süre bekleyerek tekrar kontrol etme
            await asyncio.sleep(5)  # Örnek olarak 5 dakika bekletme (saniye cinsinden)

            # Tarayıcıyı sürekli kapatıp açmak yerine mevcut açık olan sekmeyi yenileyip kontrolü sağla
            driver.refresh()

    except Exception as e:
        print(f'Hata: {str(e)}')

    finally:
        # Tarayıcıyı kapatma
        driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
