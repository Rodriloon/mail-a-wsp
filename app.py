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
import pystray
from PIL import Image, ImageDraw

GRUPO = "Sadge bob"
CHECK_INTERVAL = 30  # segundos para pruebas

class MailToWspApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail a WhatsApp")
        self.root.geometry("300x250")
        self.running = False
        self.thread = None
        self.driver = None
        self.icon = None

        self.minimize_var = tk.BooleanVar(value=True)
        self.checkbox = tk.Checkbutton(root, text="Minimizar a bandeja al cerrar", variable=self.minimize_var)
        self.checkbox.pack(padx=20, pady=(10, 0))

        self.start_btn = tk.Button(root, text="Iniciar servicio", command=self.start)
        self.start_btn.pack(padx=20, pady=10)

        self.stop_btn = tk.Button(root, text="Detener servicio", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(padx=20, pady=10)

        self.status = tk.Label(root, text="Servicio detenido")
        self.status.pack(padx=20, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if self.minimize_var.get():
            self.minimize_to_tray()
        else:
            self.root.destroy()

    def start(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status.config(text="Servicio en ejecución")
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument(r"--user-data-dir=C:\Users\rodri\OneDrive\Escritorio\mail-a-wsp\chrome_profile")
        self.driver = webdriver.Chrome(options=chrome_options)
        driver = self.driver
        driver.get("https://web.whatsapp.com")
        time.sleep(2)
        # Intentar cerrar el banner de descarga si aparece
        for _ in range(5):
            try:
                close_banner = driver.find_element(By.XPATH, '//span[@data-icon="x-viewer"]')
                close_banner.click()
                time.sleep(1)
            except Exception:
                time.sleep(1)
        self.status.config(text="Esperando login en WhatsApp Web")
        try:
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@role="textbox" and @contenteditable="true" and (' +
                               'contains(@aria-label, "Buscar") or contains(@aria-label, "Search") or ' +
                               'contains(@aria-placeholder, "Buscar un chat o iniciar uno nuevo"))]')
                )
            )
            self.status.config(text="Sesión iniciada en WhatsApp Web")
        except Exception:
            self.status.config(text="No se detectó el campo de búsqueda. Cerrá banners o recargá WhatsApp Web.")
            driver.quit()
            return

        try:
            boton_continuar = driver.find_element(By.XPATH, '//button[.//span[text()="Continuar"]]')
            boton_continuar.click()
            time.sleep(1)
        except Exception:
            pass

        enviados = set()

        while self.running:
            self.status.config(text="Revisando mails...")
            mails = obtener_contenido_mail(return_id=True)
            nuevos = []
            for contenido, mail_id in mails:
                if mail_id not in enviados:
                    nuevos.append((contenido, mail_id))
            if nuevos:
                self.status.config(text=f"Enviando {len(nuevos)} mail(s) a WhatsApp...")

                try:
                    # Volver a la pantalla principal de chats si el botón está presente
                    try:
                        back_btn = driver.find_element(By.XPATH, '//button[@aria-label="Volver" or @aria-label="Back"]')
                        back_btn.click()
                        time.sleep(1)
                    except Exception:
                        pass

                    # Buscar el grupo
                    wait = WebDriverWait(driver, 15)
                    search_box = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//div[@role="textbox" and @contenteditable="true" and (contains(@aria-label, "Buscar") or contains(@aria-label, "Search") or contains(@aria-placeholder, "Buscar un chat o iniciar uno nuevo"))]')
                    ))
                    search_box.click()
                    time.sleep(1)
                    search_box.clear()
                    search_box.send_keys(GRUPO)
                    time.sleep(2)
                    search_box.send_keys(Keys.ENTER)
                    time.sleep(3)  # Espera a que cargue el chat

                    # Esperar el cuadro de mensaje (prueba varios XPATH)
                    wait = WebDriverWait(driver, 15)
                    msg_box = None
                    for xpath in [
                        '//footer//div[@role="textbox" and @contenteditable="true"]',
                        '//div[@tabindex="10" and @contenteditable="true"]',
                        '//div[@contenteditable="true" and @data-tab]',
                        '//div[@role="textbox" and @contenteditable="true"]'
                    ]:
                        try:
                            msg_box = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                            break
                        except Exception:
                            continue
                    if not msg_box:
                        raise Exception("No se encontró el cuadro de mensaje para escribir.")

                    msg_box.click()
                    time.sleep(0.5)

                    # Enviar todos los mensajes seguidos
                    for contenido, mail_id in nuevos:
                        for linea in contenido.splitlines():
                            msg_box.send_keys(linea)
                            msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
                        msg_box.send_keys(Keys.BACKSPACE)
                        msg_box.send_keys(Keys.ENTER)
                        enviados.add(mail_id)
                        time.sleep(1)  # Pequeña pausa entre mensajes

                    # Volver a la lista de chats haciendo click en el ícono de chats de la barra lateral
                    try:
                        chats_btn = driver.find_element(By.XPATH, '//span[@data-icon="chat"]')
                        chats_btn.click()
                        time.sleep(1)
                    except Exception:
                        pass

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

    def stop(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="Servicio detenido")
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass

    def minimize_to_tray(self):
        self.root.withdraw()
        if not self.icon:
            image = Image.new('RGB', (64, 64), color='white')
            d = ImageDraw.Draw(image)
            d.ellipse((16, 16, 48, 48), fill='green')  # Simple WhatsApp-like icon
            self.icon = pystray.Icon(
                "Mail a WhatsApp",
                image,
                "Mail a WhatsApp",
                menu=pystray.Menu(
                    pystray.MenuItem("Restaurar", self.restore_window),
                    pystray.MenuItem("Salir", self.quit_app)
                ),
                # Esto permite restaurar con doble click
                on_double_click=self.restore_window
            )
        threading.Thread(target=self.icon.run, daemon=True).start()

    def restore_window(self, icon, item):
        self.root.after(0, self.root.deiconify)
        if self.icon:
            self.icon.stop()
            self.icon = None

    def quit_app(self, icon, item):
        self.root.after(0, self.root.destroy)
        if self.icon:
            self.icon.stop()
            self.icon = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MailToWspApp(root)
    root.mainloop()