"""
Módulo de Gestión de Profesores

Este módulo define la clase Profesor y las herramientas para administrar la 
nómina docente, incluyendo su carga académica máxima y las materias que 
están capacitados para dictar.
"""

from . import requests_api as api
import json

lista_final_profesor = []

class Profesor():
    """
    Representa a un docente con sus datos personales, laborales y 
    su especialización en materias.
    """
    def __init__(self, nombre, apellido, cedula, email, max_carga, materias):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.max_carga = max_carga
        self.materias = materias

    def __str__(self):
        return f"Informacion del profesor:\n\nNombre y Apellido: {self.nombre} {self.apellido}\nCedula: {self.cedula}\nCorreo: {self.email}\nCarga maxima: {self.max_carga}\nMaterias: {self.materias}"
    
    def __repr__(self):
        return (f"Profesor(nombre='{self.nombre}', apellido='{self.apellido}', "
                f"cedula={self.cedula}, max_carga={self.max_carga}, materias={self.materias})")
    
    @staticmethod
    def crear_objeto():
        """
        Carga los datos de los profesores desde el archivo JSON local.
        """
        # Con este try-except buscamos evitar que el programa se detenga si falta el archivo de base de datos, 
        # ya que alguien puede intentar iniciar el sistema sin haber descargado los datos de GitHub primero.
        try:
            lista_final_profesor.clear() # Limpieza para evitar duplicados en memoria
            with open("profesores.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                nuevo_profe = Profesor(
                    item["Nombre"],
                    item["Apellido"],
                    item["Cedula"],
                    item["Email"],
                    item["Max Carga"],
                    item["Materias"]
                )
                lista_final_profesor.append(nuevo_profe)
            return lista_final_profesor
        except FileNotFoundError:
            print("\n[!] Error: No se encontró 'profesores.json'. Use la opción 6.")
        except Exception as e:
            print(f"\n[!] Error inesperado al cargar profesores: {e}")

def ver_profesores():
    """Muestra la lista de todos los docentes registrados."""
    for i, profe in enumerate(lista_final_profesor, 1):
        print(f"{i}. {profe.nombre} {profe.apellido}")

def specific_profesor():
    """Busca un profesor por su número de cédula."""
    # Con este try-except buscamos evitar que el programa falle por un error de tipo, 
    # ya que alguien puede poner puntos o letras en el campo de la cédula.
    try:
        x = int(input("Ingrese el numero de cedula del docente: "))
        for profe in lista_final_profesor:
            if profe.cedula == x:
                return profe
        return "Profesor no encontrado."
    except ValueError:
        return "\n[!] Error: La cédula debe contener solo números."

def add_profesor():
    """Registra un nuevo profesor de forma manual."""
    # Con este try-except buscamos evitar que el programa se cierre por errores de entrada, 
    # ya que alguien puede ingresar texto en campos que requieren números (cédula o carga).
    # Con los bucle while evitamos que el usuario ingrese valores que esten vacios,
    # como pueden ser el nombre, apellido y el email.
    try:
        nombre = input("Ingrese el nombre del profesor: ")
        while nombre == "":
            nombre = input("[!] Error: Por favor ingrese un nombre valido: ")  
        apellido = input("Ingrese el apellido del profesor: ")
        while apellido == "":
            apellido = input("[!] Error: Por favor ingrese un apellido valido: ")
        cedula = int(input("Ingrese la cedula del profesor: "))
        email = input("Ingrese el correo del profesor: ")
        while email == "":
            email = input("[!] Error: Por favor ingrese un correo valido: ")
        max_carga = int(input("Ingrese la carga maxima de materias (número): "))
        
        list_materias = []
        
        for i in range(max_carga):
            #list_materias.append(input(f"Ingrese el código de la materia {i+1}: "))
            x = input(f"Ingrese el código de la materia {i+1}: ")
            while x == "":
                x = input("[!] Error: Por favor ingrese un codigo de materia valido: ")
            list_materias.append(x.upper())
        nuevo = Profesor(nombre.upper(), apellido.upper(), cedula, email.upper(), max_carga, list_materias)
        lista_final_profesor.append(nuevo)
        print("\n[ÉXITO] Profesor añadido correctamente.")
    except ValueError:
        print("\n[!] Error: Cédula y carga máxima deben ser valores numéricos.\n")

def del_profesor():
    """Elimina a un profesor de la lista tras confirmar la acción."""
    try:
        x = int(input("Ingrese la cédula del docente a eliminar: "))
        for i, profe in enumerate(lista_final_profesor):
            if x == profe.cedula:
                print(profe)
                y = input("¿Está seguro de eliminar este docente? (Y/N): ")
                if y.lower() == "y":
                    lista_final_profesor.pop(i)
                    print("El profesor ha sido eliminado.")
                    return
                else:
                    print("No se elimino el profesor")
                    return
        print("No se encontró ningún profesor con esa cédula.")
    except ValueError:
        print("\n[!] Error: Ingrese una cédula válida.")

def modlistmateriasprofe():
    """Permite añadir o quitar materias de la especialidad de un profesor."""
    try:
        x = int(input("Ingrese la cédula del docente: "))
        for profe in lista_final_profesor:
            if x == profe.cedula:
                print(profe)
                y = int(input("\n1. Agregar Materias\n2. Eliminar Materias\n3. Volver\n>> "))
                if y == 1:
                    newcod = input("Código de la nueva materia: ")
                    while newcod == "":
                        newcod = input("[!] Error: ingrese un codigo de materia valido: ")
                    profe.materias.append(newcod.upper())
                    print("Materia añadida con éxito.")
                    return
                elif y == 2:
                    cod = input("Código de la materia a eliminar: ")
                    while cod == "":
                        cod = input("[!] Error: ingrese un codigo de materia valido: ")
                    if cod in profe.materias:
                        profe.materias.remove(cod)
                        print("Materia eliminada.")
                        return
                    else:
                        print("El profesor no dicta esa materia.")
                        return
                elif y == 3:
                    return
                else:
                    print("\n[!] Error: Entrada inválida.\n")
                    return
        print("Cédula no encontrada.")
    except ValueError:
        print("\n[!] Error: Entrada inválida.\n")

# Inicialización automática
Profesor.crear_objeto()