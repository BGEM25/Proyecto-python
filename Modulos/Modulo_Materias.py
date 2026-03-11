from . import requests_api as api
from . import Modulo_Profesores

lista_final_materias = []
class Materias():
    def __init__(self, nombre, codigo, secciones):
        self.nombre = nombre
        self.codigo = codigo
        self.secciones = secciones
    
    def __str__(self):
        return f"Informacion de la materia:\n\nNombre: {self.nombre}\nCodigo: {self.codigo}\nSecciones: {self.secciones}\n"

    def crear_objeto():
        x = 0
        data = api.data_materias
        for newobject in data:
            newobject = Materias(data[x]["Nombre"],data[x]["Código"],data[x]["Secciones"])
            lista_final_materias.append(newobject)
            x += 1
        return lista_final_materias

def ver_materia():
    z = 0
    for materia in lista_final_materias:
        z += 1
        print(f"{z}",materia.nombre)

def specific_materia():
    x = input("Ingrese el codigo de la materia: ")
    for materia in lista_final_materias:
        if materia.codigo == x:
            return materia
                            

def add_materia():
    nombre = input("Ingrese el nombre de la materia: ")
    codigo = input("Ingrese el codigo de la materia: ")
    secciones = int(input("Ingrese la cantidad de secciones de la materia: "))
    newobject = Materias(nombre, codigo, secciones)
    print(newobject)
    lista_final_materias.append(newobject)

def del_materia():
    z = -1
    x = input("Ingrese el codigo de la materia a eliminar: ")
    for materia in lista_final_materias:
        z += 1
        if x == materia.codigo:
            print(materia)
            y = input("Esta seguro que quiere eliminar esta materia de la lista? (Y/N): ")
            if y == "Y" or "y":
                lista_final_materias.pop(z)
                print("La materia ha sido eliminada")
                return 
            else:
                print("No se elimino la materia de la lista")
                pass  

def modseccionmateria():
    z = -1
    x = input("Ingrese el codigo de la materia al que se le modificara el numero de secciones: ")
    for materia in lista_final_materias:
        z += 1
        if x == materia.codigo:
            print(materia)
            newsecc = int(input("Ingrese el nuevo numero de secciones: "))
            materia.secciones = newsecc
            print("Seccion cambiada con exito!\n",materia.nombre,"\n","Nuevo nro de secciones:",materia.secciones)

def materia_asociada():
        z = -1
        x = input("Ingrese el codigo de la materia para ver que profesores estan asociados: ")
        for profe in Modulo_Profesores.lista_final_profesor:
            z += 1
            if x in profe.materias:
                #print("\n",i["Nombre"], i["Apellido"],i["Cedula"],"\nLista de materias:", i["Materias"],"\n")
                print(profe.nombre, profe.apellido, profe.cedula, "\nlista de materias: ",profe.materias, "\n")
            #else:
                #print("No se encontro ningun profesor asociada a la materia",x)
                #return

    # def materia_asociada_fromapi():
    #     data = api.data_profesores
    #     z = -1
    #     x = input("Ingrese el codigo de la materia para ver que profesores estan asociados: ")
    #     for i in api.data_profesores:
    #         z += 1
    #         if x in i["Materias"]:
    #             print("\n",i["Nombre"], i["Apellido"],i["Cedula"],"\nLista de materias:", i["Materias"],"\n")
    #         #else:
    #             #print("No se encontro ningun profesor asociada a la materia",x)
    #             #return