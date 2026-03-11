from . import requests_api as api
import json

class Materias():
    def __init__(self, Código, Nombre, Secciones):
        self.codigo = Código
        self.nombre = Nombre
        self.secciones = Secciones
    
    def ver_materias_fromapi():
        x = 0
        for i in api.data_materias:
            x += 1
            #print(json.dumps(requests_api.data_profesores[:]["Nombre"], indent=2))
            print(x,i["Nombre"])

    def specific_materia_fromapi():
        x = input("Ingrese el codigo de la materia: ")
        for i in api.data_materias:
            if x == i["Código"]:
                print("Informacion de la materia:\n",json.dumps(i, indent=1))
                #return
                            
    def add_materia_fromapi():
        data = api.data_materias

        Nombre = input("Ingrese el nombre de la materia: ")
        Codigo = input("Ingrese el codigo de la materia: ")
        Secciones = int(input("Ingrese la cantidad de secciones de la materia: "))
        new_materia = {
            "Código":Codigo,
            "Nombre":Nombre,
            "Secciones":Secciones,
        }
        data.append(new_materia)
        print("Nueva materia registrada:\n",json.dumps(new_materia, indent=1), end="")

    def del_materia_fromapi():
        z = -1
        x = input("Ingrese el codigo de la materia a eliminar: ")
        for i in api.data_materias:
            z += 1
            if x == i["Código"]:
                print("Informacion de la materia:\n",json.dumps(i, indent=1), end="")
                y = input("Esta seguro que quiere eliminar esta materia de la lista? (Y/N): ")
                if y == "Y" or "y":
                    api.data_materias.pop(z)
                    return 
                else:
                    print("No se elimino la materia de la lista")
                    pass

    def modseccionmateria_fromapi():
        data = api.data_materias
        z = -1
        x = input("Ingrese el codigo de la materia al que se le modificara el numero de secciones: ")
        for i in api.data_materias:
            z += 1
            if x == i["Código"]:
                print("Informacion de la materia:\n",i["Nombre"],"\n","Secciones:",i["Secciones"])
                newsecc = int(input("Ingrese el nuevo numero de secciones: "))
                data[z]["Secciones"] = newsecc
                print("Seccion cambiada con exito!\n",i["Nombre"],"\n","Nuevo nro de secciones:",i["Secciones"])
    def materia_asociada_fromapi():
        data = api.data_profesores
        z = -1
        x = input("Ingrese el codigo de la materia para ver que profesores estan asociados: ")
        for i in api.data_profesores:
            z += 1
            if x in i["Materias"]:
                print("\n",i["Nombre"], i["Apellido"],i["Cedula"],"\nLista de materias:", i["Materias"],"\n")
            #else:
                #print("No se encontro ningun profesor asociada a la materia",x)
                #return