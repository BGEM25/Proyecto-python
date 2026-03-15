"""
Módulo de Gestión de Materias

Este módulo define la clase Materia y las funciones necesarias para administrar
el catálogo de asignaturas, permitiendo agregar, eliminar, visualizar y 
modificar la cantidad de secciones disponibles.
"""

from . import requests_api as api
from . import Modulo_Profesores
import json

lista_final_materias = []

class Materia():
    """
    Representa una asignatura del plan de estudios con su nombre, 
    código único y número de secciones a ofertar.
    """
    def __init__(self, nombre, codigo, secciones):
        self.nombre = nombre
        self.codigo = codigo
        self.secciones = secciones
    
    def __str__(self):
        return f"Informacion de la materia:\n\nNombre: {self.nombre}\nCodigo: {self.codigo}\nSecciones: {self.secciones}\n"

    def __repr__(self):
        return (f"Materia(nombre='{self.nombre}', codigo='{self.codigo}', "
                f"secciones={self.secciones})")
    
    @staticmethod
    def crear_objeto():
        """
        Lee el archivo JSON local para cargar las materias en la memoria del programa.
        """
        # Con este try-except buscamos evitar que el programa se detenga si no existe el archivo JSON,
        # ya que alguien puede haber borrado el archivo 'materias2526-1.json' accidentalmente.
        try:
            lista_final_materias.clear() # Limpiamos para evitar duplicados
            with open("materias2526-1.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            for item in data:
                new_materia = Materia(item["Nombre"], item["Código"], item["Secciones"])
                lista_final_materias.append(new_materia)
            return lista_final_materias
        except FileNotFoundError:
            print("\n[!] Error: No se encontró el archivo 'materias2526-1.json'.")
        except Exception as e:
            print(f"\n[!] Error inesperado al cargar materias: {e}")

def ver_materia():
    """Muestra la lista completa de materias cargadas actualmente."""
    for i, materia in enumerate(lista_final_materias, 1):
        print(f"{i}. {materia.nombre} ({materia.codigo})")

def specific_materia():
    """Busca y retorna los datos de una materia específica usando su código."""
    x = input("Ingrese el codigo de la materia: ")
    for materia in lista_final_materias:
        if materia.codigo == x:
            return materia
    print("Materia no encontrada.")

def add_materia():
    """Permite al usuario registrar una nueva materia manualmente."""
    # Con este try-except buscamos evitar que el programa falle por un error de valor,
    # ya que alguien puede poner letras en la cantidad de secciones.
    try:
        nombre = input("Ingrese el nombre de la materia: ")
        while nombre == "":
            nombre = input("[!] Error: Por favor ingrese un nombre valido: ")  
        codigo = input("Ingrese el codigo de la materia: ")
        while apellido == "":
            apellido = input("[!] Error: Por favor ingrese un codigo de materia valido: ")
        secciones = int(input("Ingrese la cantidad de secciones de la materia: "))
        newobject = Materia(nombre, codigo, secciones)
        lista_final_materias.append(newobject)
        print("\n[ÉXITO] Materia agregada.")
    except ValueError:
        print("\n[!] Error: Las secciones deben ser un número entero.")

def del_materia():
    """Elimina una materia y la quita de los profesores que la tengan asociada."""
    x = input("Ingrese el codigo de la materia a eliminar: ")
    materia_encontrada = None
    
    for materia in lista_final_materias:
        if materia.codigo == x:
            materia_encontrada = materia
            break
            
    if materia_encontrada:
        confirmar = input(f"Advertencia: Si elimina {x}, se quitará de los profesores asociados. ¿Continuar? (Y/N): ")
        if confirmar.lower() == 'y':
            # Limpieza en la lista de profesores
            for profe in Modulo_Profesores.lista_final_profesor:
                if x in profe.materias:
                    profe.materias.remove(x)
            # Eliminación de la lista de materias
            lista_final_materias.remove(materia_encontrada)
            print("La materia ha sido eliminada con éxito.")
    else:
        print("No se encontró ninguna materia con ese código.")

def modseccionmateria():
    """Modifica la cantidad de secciones disponibles para una materia."""
    x = input("Ingrese el codigo de la materia: ")
    for materia in lista_final_materias:
        if materia.codigo == x:
            try:
                newsecc = int(input(f"Secciones actuales ({materia.secciones}). Ingrese el nuevo nro: "))
                if newsecc == 0:
                    y = input("Al poner 0, la materia no se ofertará. ¿Continuar? (Y/N): ")
                    if y.lower() != 'y':
                        return
                materia.secciones = newsecc
                print("¡Secciones actualizadas con éxito!")
            except ValueError:
                print("Error: Ingrese un número válido.")
            return
    print("Materia no encontrada.")
                
def materia_asociada():
    """Muestra qué profesores están capacitados para dictar una materia específica."""
    x = input("Ingrese el codigo de la materia: ")
    encontrado = False
    for profe in Modulo_Profesores.lista_final_profesor:
        if x in profe.materias:
            print(f"- {profe.nombre} {profe.apellido} (CI: {profe.cedula})")
            encontrado = True
    if not encontrado:
        print("No hay profesores asociados a esta materia.")

# Carga inicial al importar el módulo
Materia.crear_objeto()