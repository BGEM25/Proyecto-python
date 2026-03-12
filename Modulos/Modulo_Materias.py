from . import requests_api as api
from . import Modulo_Profesores

lista_final_materias = []
class Materia():
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
            newobject = Materia(data[x]["Nombre"],data[x]["Código"],data[x]["Secciones"])
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
    newobject = Materia(nombre, codigo, secciones)
    print(newobject)
    lista_final_materias.append(newobject)

def del_materia():
    z = -1
    boolean = False
    x = input("Ingrese el codigo de la materia a eliminar: ")
    for materia in lista_final_materias:
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
            lista_final_materias.pop(z)
            print("La materia ha sido eliminada")
        elif boolean == False:
            print("No se elimino la materia de la lista")
            break

def modseccionmateria():
    z = -1
    x = input("Ingrese el codigo de la materia al que se le modificara el numero de secciones: ")
    for materia in lista_final_materias:
        z += 1
        if x == materia.codigo:
            print(materia)
            newsecc = int(input("Ingrese el nuevo numero de secciones: "))
            boolean = False
            if newsecc == 0:
                y = input(f"Advertencia, al ingresar el numero cero quiere referirse que la materia de codigo {materia.codigo} no se oferta en el trimestre actual\nDesea continuar? (Y/N)\n")
                if y == "Y" or y == "y":
                    boolean = True
                    materia.secciones = newsecc
                    print("Seccion cambiada con exito!\n",materia.nombre,"\n","Nuevo nro de secciones:",materia.secciones)          
            if boolean == False and newsecc == 0:
                print("No se cambio el numero de secciones")
                break
            elif newsecc != 0:
                materia.secciones = newsecc
                print("Seccion cambiada con exito!\n",materia.nombre,"\n","Nuevo nro de secciones:",materia.secciones)
                
def materia_asociada():
        z = -1
        x = input("Ingrese el codigo de la materia para ver que profesores estan asociados: ")
        for profe in Modulo_Profesores.lista_final_profesor:
            z += 1
            if x in profe.materias:
                print(profe.nombre, profe.apellido, profe.cedula, "\nlista de materias: ",profe.materias, "\n")