from Modulos import *

Modulo_Materias.Materia.crear_objeto()
Modulo_Profesores.Profesor.crear_objeto()
while True:
    x = input("1. Profesores\n2. Materias\n3. Generacion de horarios\n4. Modificacion de Horarios\n5. Crear listas en blanco\n6. Descargar los datos de la API de Github\n7. Cargar un horario en CSV\n8. Salir\n")
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
        pass
    elif x == "4":
        pass
    elif x == "5":
        pass
    elif x == "6":
        #requests_api.descargar()
        pass
    elif x == "7":
        pass
    elif x == "8":
        print("Programa finalizado")
        break
