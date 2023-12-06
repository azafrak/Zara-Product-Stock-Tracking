# Zara Ürün Stok Takibi

# CONFIG.JSON DOSYASINDA DEĞİŞTİRİLMESİ GEREKEN YERLER.

driver_path = buraya https://googlechromelabs.github.io/chrome-for-testing/ adresinden, tarayıcınızın sürümüne uygun indirdiğiniz chromedriver sürücüsünün bilgisayardaki konumunu yazılacak.  
chrome_binary_path = bu kısma bilgisayarınızda yüklü olan Chrome tarayıcısının exe adresinin yolu yazılacak.  
TELEGRAM TOKEN = yazan yere telegram botunuzun API TOKEN 'ını yazılacak.  
TELEGRAM_CHAT_ID = yazan yere telegramda ki kanalınızın CHAT ID'si yazılacak. 

"product" altında bulunan "url": ürünün linki eklenecek.  
"product_id": ürünün stok numarası  
"item_id": ürünün beden numarası.  

birden fazla URL takip edilecek ise işlemi çoğaltabilirsiniz. tek bir ürün takip edilecek ise ilgili satırları silebilirsiniz.
 

Ekran görüntülerinde web sitesi inspect edilerek hangi alanların alınacağı gösterildi.  

Bu koşullar sağlandığında kendi ürününüzün stok durumunu da kontrol ettirebilirsiniz.  

Beden bilgisini kontrol eden element product-size-selector-XXXXX buradaki XXX olan satır ürünün product_id'sidir.  
yanındaki item-1 yazan da beden numarasını temsil eder. JSON dosyasındaki ilgili yerleri takip etmek istediğiniz ürünün bilgileri ile doldurun.
![alt text](https://img001.prntscr.com/file/img001/uGXfan5USe6tLtOQR6fUqw.png)  

Proje headless modda çalışacak şekilde düzenlendi. Yani karşınıza tarayıcı aktivitesi gelmeyecek, tarayıcı arka planda çalışacaktır. 




# Zara Product Stock Tracking

# PLACES TO BE CHANGED IN THE CONFIG.JSON FILE.

driver_path = The location of the chromedriver driver on the computer that you downloaded from https://googlechromelabs.github.io/chrome-for-testing/ according to the version of your browser will be written here.  
chrome_binary_path = The path to the exe address of the Chrome browser installed on your computer will be written in this section.  
The API TOKEN of your telegram bot will be written where TELEGRAM TOKEN = is written  
The CHAT ID of your channel in Telegram will be written where TELEGRAM_CHAT_ID = 

"url" under "product": the link of the product will be added.  
"product_id": stock number of the product  
"item_id": size number of the product.  

If more than one URL will be followed, you can duplicate the process. If a single product is to be tracked, you can delete the relevant lines.  

The screenshots show which areas will be taken by inspecting the website.  

When these conditions are met, you can also check the stock status of your own product.  

The element that controls body information. The line XXX in the product-size-selector-XXXXXX section is the product_id of the product.   
The item-1 written next to it represents the body number. Fill in the relevant places in the JSON file with the information of the product you want to track.  
![alt text](https://img001.prntscr.com/file/img001/uGXfan5USe6tLtOQR6fUqw.png)  

The project was designed to run in headless mode. In other words, you will not see any browser activity, the browser will run in the background.
