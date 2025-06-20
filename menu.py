import os
import helpers
import database as db

def iniciar():
    while True :
        helpers.limpiar_pantalla()
        
        print("=============================")
        print("  Bienvenido al Gestor CRUD  ")
        print("=============================")
        print("[1] Listas los clientes      ")
        print("[2] Buscar un cliente        ")
        print("[3] Añadir un cliente        ")
        print("[4] Modificar un cliente     ")
        print("[5] Borrar un cliente        ")
        print("[6] Cerrar el programa       ")
        print("=============================")
        opcion = input("> ")
        helpers.limpiar_pantalla()
        
        if opcion == '1':
            print("Listando los clientes ... \n")
            
            for cliente in db.Clientes.lista:
                print(cliente)
                
        elif opcion == '2':
            print("Buscando los clientes ... \n")
            dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if(cliente) else print("Cliente no encontrado")
            
        elif opcion == '3':
            print("Añadiendo clientes ... \n")
            dni = None
            while True:
                dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
                if helpers.dni_valido(dni,db.Clientes.lista):
                    break
            
            nombre = helpers.leer_texto(2,30,"Nombre( 2-30 char)").capitalize()
            apellido = helpers.leer_texto(2,30,"Apellido(2-30 char)").capitalize()
            cliente = db.Clientes.crear(dni,nombre,apellido)
            print("Cliente añadido correctamente")
            
        elif opcion == '4':
            print("Modificando un cliente ... \n")
            dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2,30,f"Nombre( 2-30 char) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2,30,f"Apellido(2-30 char) [ {cliente.apellido}]").capitalize() 
                db.Clientes.modificar(dni,nombre,apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado")
            
            
        elif opcion == '5':
            print("Borrar un cliente ... \n")
            dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
            print("Cliente borrado correctamente") if db.Clientes.borrar(dni) else print("Cliente no encontrado")
            
            
        elif opcion == '6':
            print("Saliendo ... \n")
            break
        
        input("\n Presiona ENTER para continuar")