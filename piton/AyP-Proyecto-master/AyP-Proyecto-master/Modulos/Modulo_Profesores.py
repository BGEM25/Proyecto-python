from . import requests_api as api
import json

# cambiar profesores a profesor

class Profesores():
    def __init__(self, Nombre, Apellido, Cedula, Email, Max_Carga, Materias):
        self.nombre = Nombre
        self.apellido = Apellido
        self.cedula = Cedula
        self.email = Email
        self.max_carga = Max_Carga
        self.materias = Materias    

    def info_profe(self):
        print(self.nombre, self.apellido, self.cedula, self.email, self.max_carga, self.materias)

    def ver_profesores_fromapi():
        x = 0
        for i in api.data_profesores:
            x += 1
            #print(json.dumps(requests_api.data_profesores[:]["Nombre"], indent=2))
            print(x, i["Nombre"], i["Apellido"])
                            
    def add_profesor_fromapi():
        data = api.data_profesores

        Nombre = input("Ingrese el nombre del profesor: ")
        Apellido = input("Ingrese el apellido del profesor: ")
        Cedula = int(input("Ingrese la cedula del profesor: "))
        Email = input("Ingrese el correo del profesor: ")
        Max_Carga = int(input("Ingrese la carga maxima de materias del profesor: "))
        x = Max_Carga
        list_materias = []
        while x > 0:
            list_materias.append(input("Ingrese los codigos de las materias del profesor: "))
            x -= 1
        new_profesor = {
            "Cedula":Cedula,
            "Email":Email,
            "Apellido":Apellido,
            "Nombre":Nombre,
            "Max Carga":Max_Carga,
            "Materias":list_materias
        }
        data.append(new_profesor)
        print("Nuevo docente registrado:\n",json.dumps(new_profesor, indent=1), end="")

    def del_profesor_fromapi():
        z = -1
        x = int(input("Ingrese el numero de cedula del docente a eliminar: "))
        for i in api.data_profesores:
            z += 1
            if x == i["Cedula"]:
                print("Informacion del Docente:\n",json.dumps(i, indent=1), end="")
                y = input("Esta seguro que quiere eliminar este docente de la lista? (Y/N): ")
                if y == "Y" or "y":
                    api.data_profesores.pop(z)
                    return 
                else:
                    print("No se elimino el docente de la lista")
                    pass

    def modlistmateriasprofe_fromapi():
        data = api.data_profesores
        z = -1
        x = int(input("Ingrese el numero de cedula del docente al que se le modificara la lista de materias: "))
        for i in api.data_profesores:
            z += 1
            if x == i["Cedula"]:
                print("Informacion del Docente:\n",json.dumps(i["Materias"], indent=1))
                y = input("1. Agregar Materias\n2. Eliminar Materias\n3. Volver al menu anterior\n")
                if y == "1":
                    newmateria = input("Ingrese el codigo de la nueva materia: ")
                    data[z]["Materias"].append(newmateria)
                    print("Materia añadida con exito!\n",data[z]["Materias"],"\n")
                if y == "2":
                    materia = input("Ingrese el codigo de la materia a eliminar: ")
                    data[z]["Materias"].remove(materia)
                    print("Materia eliminada\n",data[z]["Materias"],"\n")
                if y == "3":
                    pass

    #reservorio_profesores = []
    #reservorio_profesores.append(crear_objeto_fromapi())      

    def __str__(self):
        return f"El profesor es {self.nombre} {self.apellido} {self.cedula} {self.email}"
                  
def crear_objeto_fromapi():
    x = 0
    reservorio_profesores = []
    data = api.data_profesores
    for newobject in data:
        newobject = Profesores(data[x]["Nombre"],data[x]["Apellido"],data[x]["Cedula"],data[x]["Email"],data[x]["Max Carga"],data[x]["Materias"])
        #newobject.info_profe()
        reservorio_profesores.append(newobject)
        x += 1
        
    return reservorio_profesores

#lista_final_profesor = crear_objeto_fromapi()
#crear_objeto()
 
def specific_profesor_fromapi():
    lista_final_profesor = crear_objeto_fromapi()
    x = int(input("Ingrese el numero de cedula del docente: "))
    for profe in lista_final_profesor:
        if profe.cedula == x:
            return profe
            