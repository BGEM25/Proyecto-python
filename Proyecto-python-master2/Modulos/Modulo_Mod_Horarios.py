from . import requests_api as api
from . import Modulo_Profesores
from . import Modulo_Materias

"""
Módulo de Modificación de Horarios
Encargado de interactuar con el usuario para reasignar profesores o bloques horarios.
"""

def iniciar_modificacion(mi_horario):
    busqueda = input("\nIngrese el nombre o código de la materia a modificar: ")
    secciones = mi_horario.obtener_secciones(busqueda)
    
    if not secciones:
        print("No se encontraron secciones asignadas para esa materia.")
        return # Sale de la función y vuelve al menú
        
    print("\nSecciones encontradas:")
    for i, sec in enumerate(secciones):
        print(f"  {i+1}. Hora: {sec['horario']} | Profe: {sec['datos']['profesor']}")
        
    try:
        opc_sec = int(input("\nSeleccione el número de la sección a modificar: ")) - 1
        if opc_sec < 0 or opc_sec >= len(secciones):
            print("Opción inválida.")
            return
            
        sec_elegida = secciones[opc_sec]
        horario_actual = sec_elegida["horario"]
        profe_actual = sec_elegida["datos"]["profesor"]
        
        # Extraemos el código limpio
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
        print("Error: Debe ingresar un número válido.")