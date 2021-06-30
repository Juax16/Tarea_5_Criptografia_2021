import imaplib
import email
from email_from_formatter import *


def recover(mail, conn):
    # Se busca en el buzón elegido (INBOX)
    # Retorna una tupla con el estado
    response_2, msg_ids = conn.search(None, '(FROM %s)' %mail)

    msg_list = msg_ids[0].split()

    if msg_list == []:
        print("  No se encontró ningún correo con los criterios de búsqueda seleccionados.\n\n")
        return False

    print("     Número de correos recuperados: " + str(len(msg_list)))
    count = 0
    
    print("     Empieza la extracción de datos\n")
    
    domain = mail.split('@')[1] 
    # Crea un archivo, si existe lo reescribe, de nombre "'msgid_'+ dominio" 
    f = open('msgid_'+ domain ,'w')


    # Se recorre cada elemento de la lista ID's, no condundir con el 'message-id'
    for id in msg_list:
        # Se deodifica de bytes a utf-8
        id_raw = id.decode()
        # Se recupera el encabezado del correo
        # Retorna un mensaje del estado de la petición y la información solicitada
        typ2, msg_data = conn.fetch(id, 'BODY.PEEK[HEADER]')
        # Se decodifica
        raw_email = msg_data[0][1].decode('utf-8')
        # Se convierte en un objeto 'Message'
        email_obj = email.message_from_string(raw_email)
        # Se selecciona el 'message-id' y se le quitan los '<' y '>' del principio y final
        msg_id = email_obj['message-id'].strip('<>')
        # Recupera todos los campos 'received' y toma el primero y el penúltimo si no es el mismo y existe
        msg_receiveds = email_obj.get_all('received')
        msg_first_received = msg_receiveds[0]
        try:
            if msg_receiveds[0] != msg_receiveds[-2] and msg_receiveds[-2]:
                msg_penultimate_received = msg_receiveds[-2]
        except:
            msg_penultimate_received = 'n/a'

            if msg_receiveds[0] != msg_receiveds[-2]:
                print('Hay solo 2 received')
            else:
                print('Hay solo 1 received')
        # Recupera el UTC
        msg_utc = msg_receiveds[0][-5:]
        # Recupera el FROM
        msg_from = email_obj['from']
        # Recupera la dirección del remitente a partir del FROM
        email_from = email_from_formatter(msg_from)
        # Imprime los datos recuperados en el archivo de texto
        f.write(msg_id + '\n' + msg_first_received + '\n' + msg_penultimate_received + '\n' + msg_utc + '\n' + msg_from + '\n' + email_from + '\n\n\n\n')


    print("\n    Fin de la recuperación para la dirección: " + mail + '\n')
    print('    Guardado en el archivo: ' + 'msgid_'+ domain)
    print("______________________________________________________________________\n")