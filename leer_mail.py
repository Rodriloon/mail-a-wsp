from imap_tools import MailBox, AND
from bs4 import BeautifulSoup

def obtener_contenido_mail():
    EMAIL = 'rodripincha7@gmail.com'
    PASSWORD = 'uowgeergdkhjsmez'
    REMITENTE_OBJETIVO = 'quantumdevsunlp@gmail.com'

    with MailBox('imap.gmail.com').login(EMAIL, PASSWORD, 'INBOX') as mailbox:
        mensajes = mailbox.fetch(AND(seen=False, from_=REMITENTE_OBJETIVO))
        for mensaje in mensajes:
            if mensaje.text:
                texto = mensaje.text.strip()
            elif mensaje.html:
                soup = BeautifulSoup(mensaje.html, "html.parser")
                texto = soup.get_text(separator="\n").strip()
            else:
                texto = None
            if texto:
                # Conserva los saltos de línea, eliminando líneas vacías
                texto_con_saltos = "\n".join([line for line in texto.splitlines() if line.strip()])
                return texto_con_saltos
    return None