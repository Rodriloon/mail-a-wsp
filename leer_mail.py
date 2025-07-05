from imap_tools import MailBox, AND
from bs4 import BeautifulSoup

def obtener_contenido_mail(return_id=False):
    EMAIL = 'ejemplo@gmail.com' # Reemplaza con tu correo electrónico
    PASSWORD = '16digitos'  # Reemplaza con tu contraseña de aplicación o contraseña de correo
    REMITENTE_OBJETIVO = 'ejemplo2@gmail.com'   # Reemplaza con el remitente del que deseas leer los correos

    with MailBox('imap.gmail.com').login(EMAIL, PASSWORD, 'INBOX') as mailbox:
        mensajes = mailbox.fetch(AND(seen=False, from_=REMITENTE_OBJETIVO))
        resultados = []
        for mensaje in mensajes:
            if mensaje.text:
                texto = mensaje.text.strip()
            elif mensaje.html:
                soup = BeautifulSoup(mensaje.html, "html.parser")
                texto = soup.get_text(separator="\n").strip()
            else:
                texto = None
            if texto:
                texto_con_saltos = "\n".join([line for line in texto.splitlines() if line.strip()])
                if return_id:
                    resultados.append((texto_con_saltos, mensaje.uid))
                else:
                    resultados.append(texto_con_saltos)
        if return_id:
            return resultados
        return resultados