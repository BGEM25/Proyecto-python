"""
Sistema de Gestión de Horarios Universitarios

Este programa es el núcleo del proyecto. Controla el flujo principal, 
coordina los módulos de profesores y materias, y gestiona la persistencia
de los horarios generados durante la sesión.

Consideraciones de eficiencia globales:
- Tiempo: O(1) para la navegación. Las sentencias if/elif del menú se 
  ejecutan en tiempo constante. El tiempo total de ejecución dependerá 
  exclusivamente de la complejidad de los módulos invocados.
- Memoria (Espacio): O(M + P + H), donde 'M' son las materias, 'P' los 
  profesores y 'H' la malla horaria generada, las cuales se mantienen 
  vivas en la memoria RAM mientras el ciclo principal esté activo.
"""

from Modulos import *

# Inicialización de objetos desde archivos locales al arrancar
Modulo_Materias.Materia.crear_objeto()
Modulo_Profesores.Profesor.crear_objeto()

# Variable global para guardar el horario y mantener la persistencia en la sesión
horario_generado = None

while True:
    """
    Ciclo principal del menú. Gestiona la interacción del usuario.
    Eficiencia: O(1) por iteración.
    """
    x = input("\n1. Profesores\n2. Materias\n3. Generacion de horarios\n4. Modificacion de Horarios\n5. Crear listas en blanco\n6. Descargar los datos de la API de Github\n7. Cargar un horario en CSV\n8. Ver estadisticas\n9. Salir\n>> ")
    
    # --- MENÚ DE PROFESORES ---
    if x == "1":
        y = input("\n1. Ver lista de profesores\n2. Ver un profesor especifico\n3. Agregar profesor a una lista\n4. Eliminar profesor de una lista\n5. Modificar lista de materias de un profesor\n6. Volver al menu anterior\n>> ")
        if y == "1":
            Modulo_Profesores.ver_profesores()
            input("\nPresione Enter para volver\n")
        elif y == "2":
            print(Modulo_Profesores.specific_profesor())
            input("\nPresione Enter para volver\n")
        elif y == "3":
            Modulo_Profesores.add_profesor()
            input("\nPresione Enter para volver\n")
        elif y == "4":
            Modulo_Profesores.del_profesor()
            input("\nPresione Enter para volver\n")
        elif y == "5":
            Modulo_Profesores.modlistmateriasprofe()
            input("\nPresione Enter para volver\n")
            
    # --- MENÚ DE MATERIAS ---
    elif x == "2":
        y = input("\n1. Ver lista de materias\n2. Ver una materia en especifico\n3. Ver profesores asociados a una materia\n4. Agregar materia a una lista\n5. Eliminar materia de una lista\n6. Modificar numero de secciones de una materia\n7. Volver al menu anterior\n>> ")
        if y == "1":
            Modulo_Materias.ver_materia()
            input("\nPresione Enter para volver\n")
        elif y == "2":
            print(Modulo_Materias.specific_materia())
            input("\nPresione Enter para volver\n")
        elif y == "3":
            Modulo_Materias.materia_asociada()
            input("Presione Enter para volver\n")
        elif y == "4":
            Modulo_Materias.add_materia()
            input("\nPresione Enter para volver\n")
        elif y == "5":
            Modulo_Materias.del_materia()
            input("\nPresione Enter para volver\n")
        elif y == "6":
            Modulo_Materias.modseccionmateria()
            input("\nPresione Enter para volver\n")

    # --- GENERACIÓN DE HORARIOS ---
    elif x == "3":
        if not Modulo_Materias.lista_final_materias or not Modulo_Profesores.lista_final_profesor:
            print("\n[!] ERROR: No hay datos cargados (Materias/Profesores).")
            print("Por favor, usa la opción 6 para descargar datos de GitHub primero.")
        else:
            print("\n--- GENERACIÓN DE HORARIOS ---")
            
            # Con este try-except buscamos evitar que el programa se cierre por un error de valor (ValueError), 
            # ya que alguien puede poner letras o símbolos en lugar de un número al ingresar los salones.
            try:
                salones = int(input("Ingrese el numero de salones disponibles por bloque: "))
                horario_generado = Modulo_Gen_Horarios.Horario(salones)
                horario_generado.generar_y_reportar()
                
                while True:
                    y = input("\n--- OPCIONES DE HORARIO ---\n1. Ver el horario de una materia\n2. Ver el horario de un profesor\n3. Ver salones asignados a una hora\n4. Guardar asignación de horarios en CSV\n5. Volver al menu anterior\n>> ")
                    
                    if y == "1":
                        busqueda = input("\nIngrese el nombre o código de la materia a buscar: ")
                        horario_generado.buscar_horario_materia(busqueda)
                        input("\nPresione Enter para continuar...")
                    elif y == "2":
                        busqueda = input("\nIngrese el nombre o apellido del profesor: ")
                        horario_generado.buscar_horario_profesor(busqueda)
                        input("\nPresione Enter para continuar...")
                    elif y == "3":
                        busqueda = input("\nIngrese el bloque de hora (Ej. 'L/M 7:00'): ")
                        horario_generado.ver_salones_hora(busqueda)
                        input("\nPresione Enter para continuar...")
                    elif y == "4":
                        horario_generado.exportar_csv()
                        input("\nPresione Enter para continuar...")
                    elif y == "5":
                        break
            except ValueError:
                print("\n[!] Error de entrada: Debe ingresar un número entero para los salones.")

    # --- MODIFICACIÓN MANUAL ---
    elif x == "4":
        if horario_generado is None:
            print("\n[!] Error: Primero debes generar un horario en la opción 3.")
        else:
            Modulo_Mod_Horarios.iniciar_modificacion(horario_generado)
            
    # --- LIMPIEZA DE MEMORIA ---
    elif x == "5":
        print("\n--- CREANDO LISTAS EN BLANCO ---")
        Modulo_Materias.lista_final_materias.clear()
        Modulo_Profesores.lista_final_profesor.clear()
        horario_generado = None 
        print("[ÉXITO] Las listas y el horario han sido borrados de la memoria.")
        input("\nPresione Enter para volver al menú principal...")
        
    # --- SINCRONIZACIÓN API GITHUB ---
    elif x == "6":
        print("\n--- DESCARGANDO DATOS DE GITHUB ---")
        
        # Con este try-except buscamos evitar que el programa se cuelgue por un error de conexión o de red, 
        # ya que alguien puede no tener internet o el servidor de GitHub puede estar caído en ese momento.
        try:
            requests_api.descargar()
            Modulo_Materias.lista_final_materias.clear()
            Modulo_Profesores.lista_final_profesor.clear()
            Modulo_Materias.Materia.crear_objeto()
            Modulo_Profesores.Profesor.crear_objeto()
            horario_generado = None 
            print("\n[ÉXITO] La memoria ha sido actualizada con los datos nuevos.")
        except Exception as e:
            print(f"\n[!] Error durante la descarga: {e}")
            print("Verifique su conexión e intente de nuevo.")
            
        input("\nPresione Enter para continuar...")
        
    # --- VISUALIZACIÓN DE ARCHIVO ---
    elif x == "7":
        json_to_csv.cargar_y_mostrar_csv()
        input("\nPresione Enter para volver al menú principal...")
        
# --- VISUALIZACIÓN DE GRAFICAS ---
    elif x == "8":
        y = input("\n--- OPCIONES DE ESTADISTICAS ---\n1. Salones ocupados por hora\n2. Porcentaje de carga maxima asignada a cada profesor\n3. Porcentaje de secciones cerradas para cada materia\n4. Volver al menu anterior\n>> ")
        if y == "1":
            print("--- GENERANDO GRAFICA... ---\n")
            try:
                Modulo_Estadisticas.grafico_salones_ocupados(horario_generado)
            except AttributeError:
                print("[! Error: No existe un horario generado")
            input("\nPresione Enter para volver\n")
        elif y == "2":
            print("--- GENERANDO GRAFICA... ---\n")
            try:
                Modulo_Estadisticas.grafico_porc_maxcarga(horario_generado)
            except AttributeError:
                print("[! Error: No existe un horario generado")
            input("\nPresione Enter para volver\n")
        elif y == "3":
            print("--- GENERANDO GRAFICA... ---\n")
            try:
                Modulo_Estadisticas.grafico_porc_secciones(horario_generado)
            except AttributeError:
                print("[! Error: No existe un horario generado")
            input("\nPresione Enter para volver\n")
        else:
            pass

    # --- SALIDA ---
    elif x == "9":
        print("\n" + "*"*45)
        print("   ¡Gracias por usar el Sistema de Horarios mi pana!")
        print("*"*45 + "\n")
        break