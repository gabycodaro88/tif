# @Autor Gaby Codaro
# @Email gabrielacodaro@gmail.com
# @GitHub https://
# @Date 2023-11-29

import json
import logging

# DEBUG = 10
# INFO = 20
# WARNING = 30
# ERROR = 40
# CRITICAL = 50

"""Definicion global del loggin de la App
    Por defecto le seteamos el nivel de log de DEBUG para ver todos los logs
"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(threadName)s - %(processName)s - %(levelname)s - %(message)s',
                    filename='logginActivity.log',
                    filemode='w')


def menu_principal(logueado):
    """ Definicion del menu principal

    Params:

    String - user-login (recibe el nombre del usuario q se encuentra logueado)
    """
    logging.info('***Menu Principal de la App***')
    print ("**MENU**")
    verificar_sesion(logueado)
    print("1- Crear Usuario")
    print("2- Iniciar Sesión")
    print("3- Salir")

def verificar_sesion(logueado):
    """"Verifica si el usuario está logueado

    Params:
    String -- logueado    
    """
    
    if (str(logueado)!='' and str(logueado)!=None):
        print("Hola "+str(logueado)+" !!")

def verificar_usuario(usuarios,user):
    """Verifica si existe el usuario en el archivo
    
    Param 
    JSON - usuarios (lista de usuarios ya creados)
    STRING - user  (nombre del usuario a verificar)
    Return Boolean - devuelve si existe o no el usuario pasado
    """
    existe = False
    for key in usuarios:
        if user in key['user']:
            existe = True            
    return existe

def password_check(passwd):
    """Modulo para verificar la seguridad de la contraseña
    
    """
    val = True
    if len(passwd) < 6:
        print('La longitud minima de la password debe ser al menos de 6 caracteres')
        val = False
    if len(passwd) > 11:
        print('La longitud máxima de la password debe ser de 10 caracteres')
        val = False
    if val:
        return val
    
def crear_usuario (usuarios):
    """Definicion de la funcion de crear usuario

    Param JSON - usuarios (recibe un archivos con los usuarios ya existentes.)
    """
   
    logging.info('***Crear Usuario***')
    existe_usuario = False
    
    ##aca chequear que el usuario ingresado no este en base hacer (otra funcion de chequeo)
    while not existe_usuario:
        user = input("Ingrese el nombre de usuario: ") # prompt
        existe_usuario = verificar_usuario(usuarios,user)
        if not existe_usuario:
            print("La password deberá tener un máximo de 10 caracteres y un mínimo de 6")
            password = input("Ingrese la contraseña: ")
            if (password_check(password)):
                print("La Password es valida")
                filename = 'usuarios.txt'
                with open(filename) as fp:
                    listObj = json.load(fp)
                listObj.append({
                            "user": str(user),
                            "password": str(password)
                })
                with open(filename, 'w') as json_file:
                    json.dump(listObj, json_file, 
                                        indent=4,  
                                        separators=(',',': '))
                existe_usuario = True
                print("El usuario "+str(user)+" fue agregado correctamente")
            else:
                print("La Password no cumple con los requisitos.")
                continue
        else:      
            print("El usuario "+user+" ya existe!")
            input('\nENTER para continuar\n')
        continue
        

def iniciar_sesion(usuarios):
    """Definicion de la funcion de inicio de sesion
    Param JSON - usuarios
    Return STRING - logueado
    
    """
    logueado = ""
    existe_usuario = False
    logging.info('***Inicio de Sesion***')
    print("**Iniciar sesion**")
    user = input("Ingrese el nombre de usuario: ") # prompt
    #al ingresar el usuario se debe verificar que no exita.
    #en caso de que no exista se solicita la password
    existe_usuario = verificar_usuario(usuarios,user)
    if existe_usuario:
        for key in usuarios:
            if user in key['user']:
                #print('El usuario ya existe!')
                intentos = 3
                password = input("Ingrese la contraseña ("+str(intentos)+" intentos): ") # prompt
                intentos -= 1
                ## chequear que la pass coincida  
                if password == key['password']:
                    print("**Sesion Iniciada para el usuario: "+user+" **")
                    logueado = user
                    logging.info('***Inicio de Sesion exitoso! ('+user+')***')
                else:
                    print("Contraseña incorrecta!")
                    password = input("Ingrese la contraseña ("+str(intentos)+" intentos): ") # prompt
                    intentos -= 1
                    ## chequear que la pass coincida
                    if password == key['password']:
                        print("**Sesion Iniciada para el usuario: "+user+" **")
                        logueado = user
                        logging.info('***Inicio de Sesion exitoso! ('+user+')***')
                    else:
                        password = input("Ingrese la contraseña ("+str(intentos)+" intentos): ") # prompt
                        intentos -= 1
                        ## chequear que la pass coincida
                        if password == key['password']:
                            print("**Sesion Iniciada para el usuario: "+user+" **")
                            logueado = user
                            logging.info('***Inicio de Sesion exitoso! ('+user+')***')
                        else:
                            print("**Contraseña Inválida**")
                            logging.info('***Inicio de Sesion fallido!!***')            
    else:
        print("El usuario ingresado ("+str(user)+") no existe.")
    return logueado

       
def leer_usuarios():
    """Definicion de la funcion de leer los usuarios ya existentes

    Return JSON - datos (devuelve en esa variable los datos de los usuarios ya existentes)
    
    """
    try:
        with open('usuarios.txt', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        datos = {}
    return datos

###########################################################
###                  ESTRUCTURA PRINCIPAL               ###
###########################################################
logueado=''
opcion = ''
while opcion != '3':
    usuarios = leer_usuarios()
    menu_principal(logueado)
    opcion = input("Opción: ") # prompt
    if opcion == "1": 
        logueado = ""
        crear_usuario(usuarios)
    elif opcion == "2": 
        logueado = iniciar_sesion(usuarios)
    elif opcion == "3":
        if logueado !='':
            print ("**Adios "+logueado+"!!!**")
        else:
            print ("**Salió con éxito de la app!!**")
    else:
        print ("**Opción inválida, por favor intente nuevamente.**")
print ("**Gracias**")

