from imap_tools import MailBox, AND

# DATOS DE ACCESO
EMAIL = 'rodripincha7@gmail.com'
PASSWORD = 'uowgeergdkhjsmez'  # la contraseña de aplicación de 16 dígitos
REMITENTE_OBJETIVO = 'quantumdevsunlp@gmail.com'  # la persona que querés filtrar

# Conectarse al buzón de entrada
with MailBox('imap.gmail.com').login(EMAIL, PASSWORD, 'INBOX') as mailbox:
    # Buscar mails NO LEÍDOS y del remitente específico
    mensajes = mailbox.fetch(AND(seen=False, from_=REMITENTE_OBJETIVO))

    for mensaje in mensajes:
        print("------")
        print("Asunto:", mensaje.subject)
        print("Fecha:", mensaje.date)
        print("Contenido:")
        print(mensaje.text or mensaje.html)