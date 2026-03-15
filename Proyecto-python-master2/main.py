from Modulos import *

Modulo_Materias.Materia.crear_objeto()
Modulo_Profesores.Profesor.crear_objeto()
from Modulos import Modulo_Gen_Horarios
from Modulos import Modulo_Mod_Horarios
from Modulos import json_to_csv

# Variable global para guardar el horario y que no se borre al salir de la opción 3
horario_generado = None

while True:
    x = input("1. Profesores\n2. Materias\n3. Generacion de horarios\n4. Modificacion de Horarios\n5. Crear listas en blanco\n6. Descargar los datos de la API de Github\n7. Cargar un horario en CSV\n8. Salir\n>> ")
    
    if x == "1":
        y = input("\n1. Ver lista de profesores\n2. Ver un profesor especifico\n3. Agregar profesor a una lista\n4. Eliminar profesor de una lista\n5. Modificar lista de materias de un profesor\n6. Volver al menu anterior\n")
        if y == "1":
            print("Lista de Profesores:")
            Modulo_Profesores.ver_profesores()
            input("\nPresione Enter para volver\n")
        if y == "2":
            print(Modulo_Profesores.specific_profesor())
            input("\nPresione Enter para volver\n")
        if y == "3":
            Modulo_Profesores.add_profesor()
            input("\nPresione Enter para volver\n")
        if y == "4":
            Modulo_Profesores.del_profesor()
            input("\nPresione Enter para volver\n")
        if y == "5":
            Modulo_Profesores.modlistmateriasprofe()
            input("\nPresione Enter para volver\n")
        if y == "6":
            pass
            
    elif x == "2":
        y = input("\n1. Ver lista de materias\n2. Ver una materia en especifico\n3. Ver profesores asociados a una materia\n4. Agregar materia a una lista\n5. Eliminar materia de una lista\n6. Modificar numero de secciones de una materia\n7. Volver al menu anterior\n")
        if y == "1":
            Modulo_Materias.ver_materia()
            input("\nPresione Enter para volver\n")
        if y == "2":
            print(Modulo_Materias.specific_materia())
            input("\nPresione Enter para volver\n")
        if y == "3":
            Modulo_Materias.materia_asociada()
            input("Presione Enter para volver\n")
        if y == "4":
            Modulo_Materias.add_materia()
            input("\nPresione Enter para volver\n")
        if y == "5":
            Modulo_Materias.del_materia()
            input("\nPresione Enter para volver\n")
        if y == "6":
            Modulo_Materias.modseccionmateria()
            input("\nPresione Enter para volver\n")
        if y == "7":
            pass
            
    elif x == "3":
        if not Modulo_Materias.lista_final_materias or not Modulo_Profesores.lista_final_profesor:
            print("\n[!] ERROR: No hay datos cargados (Materias/Profesores).")
            print("Por favor, usa la opción 6 para descargar datos de GitHub primero.")
        else:
            print("\n--- GENERACIÓN DE HORARIOS ---")
            salones = int(input("Ingrese el numero de salones disponibles por bloque: "))
            horario_generado = Modulo_Gen_Horarios.Horario(salones)
            horario_generado.generar_y_reportar()
        
        while True:
            y = input("\n--- OPCIONES DE HORARIO ---\n1. Ver el horario de una materia\n2. Ver el horario de un profesor\n3. Ver salones asignados a una hora\n4. Guardar asignación de horarios en CSV\n5. Volver al menu anterior\n>> ")
            
            if y == "1":
                busqueda = input("\nIngrese el nombre o código de la materia a buscar: ")
                print("-" * 40)
                horario_generado.buscar_horario_materia(busqueda)
                print("-" * 40)
                input("\nPresione Enter para continuar...")
                
            if y == "2":
                busqueda = input("\nIngrese el nombre o apellido del profesor: ")
                print("-" * 40)
                horario_generado.buscar_horario_profesor(busqueda)
                print("-" * 40)
                input("\nPresione Enter para continuar...")
                
            if y == "3":
                busqueda = input("\nIngrese el bloque de hora (Ej. 'L/M 7:00' o '10:30'): ")
                print("-" * 40)
                horario_generado.ver_salones_hora(busqueda)
                print("-" * 40)
                input("\nPresione Enter para continuar...")
                
            if y == "4":
                horario_generado.exportar_csv()
                input("\nPresione Enter para continuar...")
                
            if y == "5":
                break
                
    elif x == "4":
        # Validamos que el horario ya se haya generado en la opción 3
        if horario_generado is None:
            print("\n[!] Error: Primero debes generar un horario en la opción 3.")
        else:
            # Llamamos al nuevo módulo pasándole el horario
            Modulo_Mod_Horarios.iniciar_modificacion(horario_generado)
            
    elif x == "5":
        print("\n--- CREANDO LISTAS EN BLANCO ---")
        Modulo_Materias.lista_final_materias.clear()
        Modulo_Profesores.lista_final_profesor.clear()
        
        # ---> LA LÍNEA MÁGICA QUE FALTABA <---
        horario_generado = None 
        
        print("[ÉXITO] Las listas y el horario han sido borrados de la memoria.")
        input("\nPresione Enter para volver al menú principal...")
        
    elif x == "6":
        print("\n--- DESCARGANDO DATOS DE GITHUB ---")
        try:
            requests_api.descargar()
            
            Modulo_Materias.lista_final_materias.clear()
            Modulo_Profesores.lista_final_profesor.clear()
            
            Modulo_Materias.Materia.crear_objeto()
            Modulo_Profesores.Profesor.crear_objeto()
            
            # ---> AQUÍ TAMBIÉN <---
            # Si descargamos datos nuevos, el horario viejo ya no sirve y hay que matarlo
            horario_generado = None 
            
            print("\n[ÉXITO] La memoria ha sido actualizada con los datos nuevos.")
            
        except Exception as e:
            print(f"\n[!] Ocurrió un error inesperado al actualizar: {e}")
            
        input("\nPresione Enter para continuar...")
        
    elif x == "7":
        json_to_csv.cargar_y_mostrar_csv()
        input("\nPresione Enter para volver al menú principal...")
        
    elif x == "8":
        print("\n" + "*"*40)
        print("  ¡Gracias por usar el Sistema de Horarios mi estimago amigo!")
        print("*"*40 + "\n")
        break  # Este es el que rompe el bucle while y cierra el program

  
