from Modulos import *

Modulo_Materias.Materias.crear_objeto()
Modulo_Profesores.Profesor.crear_objeto()

def del_materia():
    z = -1
    boolean = False
    x = input("Ingrese el codigo de la materia a eliminar: ")
    for materia in Modulo_Materias.lista_final_materias:
        z += 1
        for profe in Modulo_Profesores.lista_final_profesor:
            if x == materia.codigo and x in profe.materias:
                if boolean == False:
                    print(f"test, {materia.codigo},{profe.materias}")
                    asdf = input(f"Advertencia, existen profesores con la materia de codigo {x} asociada\nsi elimina esta materia tambien se eliminara de los profesores asociados\nContinuar? (Y/N)\n")
                if asdf == "Y" or asdf == "y":
                    boolean = True
                    profe.materias.remove(x)
                else:
                    break
        if x == materia.codigo and boolean == True:
            Modulo_Materias.lista_final_materias.pop(z)
            print("La materia ha sido eliminada")
        elif boolean == False:
            print("No se elimino la materia de la lista")
            break
            # Nótese que si se elimina una materia, deberá eliminarse de las listas de todos los 
            # profesores que la tengan. Si esto deja a uno o más profesores sin materias, debe imprimirse 
            # un mensaje de advertencia y solicitarle al usuario que confirme la acción. 


            # Nótese que al eliminar profesores o eliminar una materia de la lista de un profesor, puede 
            # quedar una materia sin profesores que puedan darla. Si esto ocurre, debe imprimirse un 
            # mensaje de advertencia y solicitarle al usuario que confirme la acción.
                # delmateria = input("Ingrese el codigo de la materia a eliminar: ")
                # profe.materias.remove(delmateria)
                # print("Materia eliminada\n",profe.materias,"\n")


del_materia()
Modulo_Materias.materia_asociada()
