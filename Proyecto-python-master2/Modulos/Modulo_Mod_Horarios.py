"""
Módulo de Modificación de Horarios

Este módulo permite al usuario realizar ajustes manuales sobre un horario 
ya generado, permitiendo cambiar tanto al profesor asignado como el bloque 
horario, validando siempre la disponibilidad de ambos.
"""

from . import requests_api as api
from . import Modulo_Profesores
from . import Modulo_Materias

def iniciar_modificacion(mi_horario):
    """
    Gestiona el proceso de búsqueda y cambio de datos de una sección específica.
    
    Args:
        mi_horario (Horario): El objeto horario que contiene la malla actual.
    """
    busqueda = input("\nIngrese el nombre o código de la materia a modificar: ")
    secciones = mi_horario.obtener_secciones(busqueda)
    
    if not secciones:
        print("No se encontraron secciones asignadas para esa materia.")
        return 
        
    print("\nSecciones encontradas:")
    for i, sec in enumerate(secciones):
        print(f"  {i+1}. Hora: {sec['horario']} | Profe: {sec['datos']['profesor']}")
        
    # Con este try-except buscamos evitar que el programa se detenga por un error de tipo (ValueError), 
    # ya que alguien puede poner letras o dejar vacío el espacio al seleccionar el número de sección.
    try:
        opc_sec = int(input("\nSeleccione el número de la sección a modificar: ")) - 1
        if opc_sec < 0 or opc_sec >= len(secciones):
            print("Opción inválida.")
            return
            
        sec_elegida = secciones[opc_sec]
        horario_actual = sec_elegida["horario"]
        profe_actual = sec_elegida["datos"]["profesor"]
        
        # Con este try-except buscamos evitar que el programa falle por un error de índice (IndexError), 
        # ya que alguien puede tener un formato de texto inesperado en el campo de materia.
        try:
            codigo_mat = sec_elegida["datos"]["materia"].split("Codigo materia: ")[1].strip()
        except IndexError:
            codigo_mat = busqueda
            
        accion = input("\n¿Qué desea hacer?\n a. Cambiar el profesor\n b. Cambiar el horario\n>> ").lower()
        
        if accion == "a":
            profes = mi_horario.obtener_profesores_libres(codigo_mat, horario_actual, profe_actual)
            if not profes:
                print("No hay profesores disponibles a esta hora.")
            else:
                for i, p in enumerate(profes):
                    print(f"  {i+1}. {p.nombre} {p.apellido} (Carga disp: {p.max_carga})")
                
                # Nuevamente validamos que la selección del nuevo profesor sea un número
                opc_profe = int(input("\nSeleccione el nuevo profesor: ")) - 1
                mi_horario.aplicar_modificacion(horario_actual, sec_elegida["indice"], horario_actual, profes[opc_profe], profe_actual)
                print("\n[ÉXITO] Profesor cambiado correctamente.")
                
        elif accion == "b":
            horas_libres = [h for h, clases in mi_horario.bloques_clases.items() if len(clases) < mi_horario.max_secciones and h != horario_actual]
            
            if not horas_libres:
                print("No hay salones disponibles en otras horas.")
            else:
                print("\nHorarios disponibles:")
                for i, h in enumerate(horas_libres):
                    print(f"  {i+1}. {h}")
                
                # Validamos que la selección del nuevo horario sea un número
                opc_hora = int(input("\nSeleccione el nuevo horario: ")) - 1
                nueva_hora = horas_libres[opc_hora]
                
                print(f"\nBuscando profesores para el bloque {nueva_hora}...")
                profes = mi_horario.obtener_profesores_libres(codigo_mat, nueva_hora, profe_actual)
                
                if not profes:
                    print("No hay profesores capacitados que puedan darla a esa hora.")
                else:
                    for i, p in enumerate(profes):
                        print(f"  {i+1}. {p.nombre} {p.apellido}")
                    opc_profe = int(input("\nSeleccione el profesor para esta nueva hora: ")) - 1
                    
                    mi_horario.aplicar_modificacion(horario_actual, sec_elegida["indice"], nueva_hora, profes[opc_profe], profe_actual)
                    print("\n[ÉXITO] Horario y profesor actualizados correctamente.")
        else:
            print("Opción inválida.")
            
    except ValueError:
        print("\n[!] Error: Debe ingresar el número de la opción deseada (no se admiten letras).")