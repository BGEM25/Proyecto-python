from . import requests_api as api

lista_final_profesor = []
class Profesor():
    def __init__(self, nombre, apellido, cedula, email, max_carga, materias):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.max_carga = max_carga
        self.materias = materias

    def __str__(self):
        return f"Informacion del profesor:\n\nNombre y Apellido: {self.nombre} {self.apellido}\nCedula: {self.cedula}\nCorreo: {self.email}\nCarga maxima de notas: {self.max_carga}\nMaterias: {self.materias}"
    
    #def info_profe(self):
    #    print(f"Informacion del profesor:\n\nNombre y Apellido:{self.nombre} {self.apellido}\nCedula: {self.cedula}\nCorreo: {self.email}\nCarga maxima de notas: {self.max_carga}\nMaterias: {self.materias}")

    def crear_objeto():
        x = 0
        data = api.data_profesores
        for newobject in data:
            newobject = Profesor(data[x]["Nombre"],data[x]["Apellido"],data[x]["Cedula"],data[x]["Email"],data[x]["Max Carga"],data[x]["Materias"])
            lista_final_profesor.append(newobject)
            x += 1
        return lista_final_profesor
 
def ver_profesores():
    z = 0
    for profe in lista_final_profesor:
        z += 1
        print(f"{z}",profe.nombre,profe.apellido)

def specific_profesor():
    x = int(input("Ingrese el numero de cedula del docente: "))
    for profe in lista_final_profesor:
        if profe.cedula == x:
            return profe
            
def add_profesor():
    nombre = input("Ingrese el nombre del profesor: ")
    apellido = input("Ingrese el apellido del profesor: ")
    cedula = int(input("Ingrese la cedula del profesor: "))
    email = input("Ingrese el correo del profesor: ")
    max_carga = int(input("Ingrese la carga maxima de materias del profesor: "))
    x = max_carga
    list_materias = []
    while x > 0:
        list_materias.append(input("Ingrese los codigos de las materias del profesor: "))
        x -= 1
    newobject = Profesor(nombre, apellido, cedula, email, max_carga, list_materias)
    print(newobject)
    lista_final_profesor.append(newobject)
    
def del_profesor():
    z = -1
    x = int(input("Ingrese el numero de cedula del docente a eliminar: "))
    for profe in lista_final_profesor:
        z += 1
        if x == profe.cedula:
            print(profe)
            y = input("Esta seguro que quiere eliminar este docente de la lista? (Y/N): ")
            if y == "Y" or "y":
                lista_final_profesor.pop(z)
                print("El profesor ha sido eliminado")
                return 
            else:
                print("No se elimino el docente de la lista")
                pass  
            
# Nótese que al eliminar profesores o eliminar una materia de la lista de un profesor, puede 
# quedar una materia sin profesores que puedan darla. Si esto ocurre, debe imprimirse un 
# mensaje de advertencia y solicitarle al usuario que confirme la acción.

def modlistmateriasprofe():
    z = -1
    x = int(input("Ingrese el numero de cedula del docente al que se le modificara la lista de materias: "))
    for profe in lista_final_profesor:
        z += 1
        if x == profe.cedula:
            print(profe)
            y = input("1. Agregar Materias\n2. Eliminar Materias\n3. Volver al menu anterior\n")
            if y == "1":
                newmateria = input("Ingrese el codigo de la nueva materia: ")
                profe.materias.append(newmateria)
                print("Materia añadida con exito!\n",profe.materias,"\n")
            if y == "2":
                delmateria = input("Ingrese el codigo de la materia a eliminar: ")
                profe.materias.remove(delmateria)
                print("Materia eliminada\n",profe.materias,"\n")
            if y == "3":
                pass