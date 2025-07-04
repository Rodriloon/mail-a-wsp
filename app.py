import threading
import time
import tkinter as tk
from tkinter import messagebox
from leer_mail import obtener_contenido_mail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GRUPO = "Sadge bob"
CHECK_INTERVAL = 30  # segundos para pruebas

class MailToWspApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail a WhatsApp")
        self.running = False
        self.thread = None

        self.start_btn = tk.Button(root, text="Iniciar servicio", command=self.start)
        self.start_btn.pack(padx=20, pady=10)

        self.stop_btn = tk.Button(root, text="Detener servicio", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(padx=20, pady=10)

        self.status = tk.Label(root, text="Servicio detenido")
        self.status.pack(padx=20, pady=10)

    def start(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status.config(text="Servicio en ejecución")
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="Servicio detenido")

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument(r"--user-data-dir=C:\Users\rodri\OneDrive\Escritorio\mail-a-wsp\chrome_profile")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.whatsapp.com")
        self.status.config(text="Esperando login en WhatsApp Web...")
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-placeholder="Buscar un chat o iniciar uno nuevo"]')))
        self.status.config(text="Sesión iniciada en WhatsApp Web")

        try:
            boton_continuar = driver.find_element(By.XPATH, '//button[.//span[text()="Continuar"]]')
            boton_continuar.click()
            time.sleep(1)
        except Exception:
            pass

        ultimo_mail = None

        while self.running:
            self.status.config(text="Revisando mails...")
            mails = obtener_contenido_mail(return_id=True)
            nuevos = []
            for contenido, mail_id in mails:
                if mail_id != ultimo_mail:
                    nuevos.append((contenido, mail_id))
            if nuevos:
                self.status.config(text=f"Enviando {len(nuevos)} mail(s) a WhatsApp...")
                for contenido, mail_id in nuevos:
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
                        msg_box = wait.until(EC.presence_of_element_located((By.XPATH, '//footer//div[@role="textbox" and @contenteditable="true"]')))
                        msg_box.click()
                        time.sleep(0.5)
                        for linea in contenido.splitlines():
                            msg_box.send_keys(linea)
                            msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
                        msg_box.send_keys(Keys.BACKSPACE)
                        msg_box.send_keys(Keys.ENTER)
                        ultimo_mail = mail_id
                    except Exception as e:
                        self.status.config(text=f"Error enviando mensaje: {e}")
            else:
                self.status.config(text="Sin mails nuevos.")
            for _ in range(CHECK_INTERVAL):
                if not self.running:
                    break
                time.sleep(1)
        driver.quit()
        self.status.config(text="Servicio detenido")

if __name__ == "__main__":
    root = tk.Tk()
    app = MailToWspApp(root)
    root.mainloop()