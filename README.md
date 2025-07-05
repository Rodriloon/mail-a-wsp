# Mail a WhatsApp

Esta aplicación permite reenviar automáticamente correos electrónicos a un grupo de WhatsApp usando una interfaz gráfica sencilla y ejecutándose en segundo plano (bandeja del sistema).

## Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/downloads) compatible con tu versión de Chrome
- Paquetes Python (ver abajo)

## Instalación

1. **Clona o descarga este repositorio.**

2. **Instala las dependencias:**
   
   Abre una terminal en la carpeta del proyecto y ejecuta:
   ```
   pip install -r requirements.txt
   ```

   Si no tienes `requirements.txt`, instala manualmente:
   ```
   pip install selenium pystray pillow imap-tools beautifulsoup4
   ```

3. **Configura ChromeDriver:**
   - Descarga el ejecutable de ChromeDriver y colócalo en la misma carpeta del proyecto o en una ruta incluida en tu PATH.

4. **Configura tu cuenta de correo en `leer_mail.py`:**
   - Edita el archivo y coloca tu email, contraseña de aplicación y remitente objetivo.

5. **Primer uso:**
   - Ejecuta el programa con:
     ```
     python app.py
     ```
   - La primera vez, inicia sesión en WhatsApp Web manualmente si es necesario.

## Uso

- **Iniciar servicio:**  
  Haz clic en "Iniciar servicio" para comenzar a monitorear el correo y reenviar mensajes a WhatsApp.

- **Minimizar a bandeja:**  
  Si marcas "Minimizar a bandeja al cerrar", al cerrar la ventana la app quedará en segundo plano (icono verde abajo a la derecha).  
  Haz doble clic en el icono para restaurar la ventana o usa el menú con clic derecho.

- **Detener servicio:**  
  Haz clic en "Detener servicio" para finalizar el monitoreo y cerrar WhatsApp Web.

## Notas

- El navegador Chrome se abrirá en modo invisible ("headless") y no molestará al usuario.
- Si necesitas escanear el QR de WhatsApp, desactiva temporalmente el modo headless (quita o comenta la línea `chrome_options.add_argument("--headless=new")` en `app.py`).
- El grupo de WhatsApp debe existir y el nombre debe coincidir exactamente con el configurado en la variable `GRUPO` de `app.py`.

## Empaquetado como .exe (opcional)

Si quieres generar un ejecutable para Windows:

1. Instala PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Ejecuta:
   ```
   pyinstaller --onefile --windowed app.py
   ```
3. El ejecutable estará en la carpeta `dist`.

---

**¡Listo! Ahora tu app reenviará automáticamente los mails a tu grupo de WhatsApp.**
