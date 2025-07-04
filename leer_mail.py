from imap_tools import MailBox, AND

def obtener_contenido_mail():
    EMAIL = 'rodripincha7@gmail.com'
    PASSWORD = 'uowgeergdkhjsmez'
    REMITENTE_OBJETIVO = 'quantumdevsunlp@gmail.com'

    with MailBox('imap.gmail.com').login(EMAIL, PASSWORD, 'INBOX') as mailbox:
        mensajes = mailbox.fetch(AND(seen=False, from_=REMITENTE_OBJETIVO))
        for mensaje in mensajes:
            return mensaje.text or mensaje.html  # Solo el primer mail no leído
    return None