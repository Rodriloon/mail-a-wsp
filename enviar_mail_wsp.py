from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Importar la función del otro archivo
from leer_mail import obtener_contenido_mail

# CONFIGURACIÓN
GRUPO = "Sadge bob"  # ← Asegurate que sea EXACTAMENTE el nombre del grupo

# Obtener el mensaje desde el mail
MENSAJE = obtener_contenido_mail()
if not MENSAJE:
    MENSAJE = "No hay mails nuevos del remitente."

# Iniciar navegador con perfil de usuario
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\Users\rodri\OneDrive\Escritorio\mail-a-wsp\chrome_profile")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")
# Esperar al escaneo del QR
print("⏳ Escaneá el código QR en WhatsApp Web...")
# Esperar hasta que la barra de búsqueda esté disponible (lo que indica que ya estás logueado)
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-placeholder="Buscar un chat o iniciar uno nuevo"]')))
print("✅ Sesión iniciada en WhatsApp Web.")

# Cerrar el cartel emergente si aparece
try:
    boton_continuar = driver.find_element(By.XPATH, '//button[.//span[text()="Continuar"]]')
    boton_continuar.click()
    time.sleep(1)
except Exception:
    pass  # Si no aparece el cartel, sigue normalmente

try:
    # Buscar la barra de búsqueda
    search_box = driver.find_element(By.XPATH, '//div[@aria-placeholder="Buscar un chat o iniciar uno nuevo"]')
    search_box.click()
    time.sleep(1)
    search_box.clear()
    search_box.send_keys(GRUPO)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Buscar el cuadro de mensaje del chat (no el de búsqueda)
    wait = WebDriverWait(driver, 15)
    msg_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//footer//div[@role="textbox" and @contenteditable="true"]')
    ))
    print("🟢 Cuadro de mensaje encontrado:", msg_box.get_attribute("aria-label"))
    msg_box.click()
    time.sleep(0.5)
    msg_box.send_keys(MENSAJE)
    time.sleep(0.5)
    msg_box.send_keys(Keys.ENTER)
    print("✅ Mensaje enviado con éxito.")

except Exception as e:
    print("❌ Ocurrió un error al buscar o enviar el mensaje.")
    print("🔎 Detalles:", e)

# Esperar antes de cerrar el navegador
time.sleep(5)
driver.quit()