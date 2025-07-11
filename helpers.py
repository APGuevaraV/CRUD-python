import os
import platform
import re

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system("clear")
    
    
def leer_texto(longitud_min = 0, longitud_max = 100, mensaje =None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max :
            return texto
    
    
def dni_valido(dni,list_clientes):
    if not re.match('[0-9]{2}[A-Z]$',dni):
        print("DNI incorrecto, debe cumplir el formato")
        return False
    for cliente in list_clientes:
        if cliente.dni == dni:
            print("DNI ya ingresado")
            return False
    return True