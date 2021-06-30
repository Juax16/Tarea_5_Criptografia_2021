import imaplib
import sys
from recover import *

FILE_NAME = 'mail_address' # Nombre del archivo con las direcciones a analizar

# Datos del usuario (dirección de correo y contraseña)
cred = open('credentials', 'r')

lines = cred.readlines()

USR_EMAIL = lines[0].strip('\n') # Correo electrónico
USR_PW = lines[1] # Contraseña del correo electrónico


# Hostname del servicio de correo, Dirección IMAP
HOSTNAME = 'imap-mail.outlook.com' # Si es Hotmail/Outlook, Gmail = 'imap.gmail.com'


# Arreglo de 2 dimensiones para guardar los datos del archivo FILENAME

lista = [[]] 

# Se recuperan las direcciones en el archivo y se depliega un menú para elegir una o todas las direcciones

with open(FILE_NAME, newline='') as file:
    data = file.readlines()
    number = 1
    print("\n Elija una de las siguientes direcciones: ")
    for row in data:
        if row == '':
            break
        row = row.strip("\r\n")
        print( '  ' + str(number)+ ') ' + row)
        lista[number-1].append(row)  
        number += 1 
        lista.append([])
print( '  ' + str(number)+ ') ' + 'Todas')

print('\n Escriba el número correspondiente a la dirección de correo elegida: ')
num = input()

while True:
    if num.isnumeric():
        if int(num) < 1 or int(num) > number:
            print("Entrada inválida, por favor ingrese un numero válido.")
            num = input()
        else:
            break
    else:
        print("Entrada inválida, por favor ingrese un numero válido.")
        num = input()



# Conexión con el servicio
conn = imaplib.IMAP4_SSL(HOSTNAME)

# Inicio de sesión
try:
    conn.login(USR_EMAIL, USR_PW)
    print("Se inició sesión correctamente!")
except:
    print("Error al iniciar sesión, se recomienda revisar los datos de ingreso.")
    sys.exit()

# Se selecciona la bandeja de entrada
response, data = conn.select('INBOX')
if response:
    print("Se seleccionó la bandeja de entrada.\n")

# Dependiendo de si se eligió una o todas, se recupera/n la/s direccion/es
# Se llama la función que extrae la información y la alamacena en un archivo de texto
if number == int(num):
    for i in range(number-1):
        print("______________________________________________________________________")
        address = lista[i][0]
        print('\n Dirección: ' + lista[i][0])
        recover(address, conn)
else:
    print("______________________________________________________________________")
    address = lista[int(num)-1][0]
    print('\n Dirección: ' + address)
    recover(address, conn)

# Se cierra la conexión
conn.close()

print('Cerrada la conexión con el servidor.')