import time
from leer_mail import obtener_contenido_mail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GRUPO = "Sadge bob"
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\Users\rodri\OneDrive\Escritorio\mail-a-wsp\chrome_profile")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")
print("⏳ Escaneá el código QR en WhatsApp Web...")
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-placeholder="Buscar un chat o iniciar uno nuevo"]')))
print("✅ Sesión iniciada en WhatsApp Web.")

# Cerrar el cartel emergente si aparece
try:
    boton_continuar = driver.find_element(By.XPATH, '//button[.//span[text()="Continuar"]]')
    boton_continuar.click()
    time.sleep(1)
except Exception:
    pass

ultimo_mail = None

while True:
    print("🔄 Revisando mails...")
    contenido, mail_id = obtener_contenido_mail(return_id=True)
    if contenido and mail_id != ultimo_mail:
        print("✉️ Nuevo mail encontrado, enviando a WhatsApp...")
        try:
            search_box = driver.find_element(By.XPATH, '//div[@aria-placeholder="Buscar un chat o iniciar uno nuevo"]')
            search_box.click()
            time.sleep(1)
            search_box.clear()
            search_box.send_keys(GRUPO)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)

            wait = WebDriverWait(driver, 15)
            msg_box = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//footer//div[@role="textbox" and @contenteditable="true"]')
            ))
            msg_box.click()
            time.sleep(0.5)
            for linea in contenido.splitlines():
                msg_box.send_keys(linea)
                msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
            msg_box.send_keys(Keys.BACKSPACE)
            msg_box.send_keys(Keys.ENTER)
            print("✅ Mensaje enviado con éxito.")
            ultimo_mail = mail_id
        except Exception as e:
            print("❌ Error enviando mensaje:", e)
    else:
        print("⏳ Sin mails nuevos.")
    time.sleep(300)  # Espera 5 minutos