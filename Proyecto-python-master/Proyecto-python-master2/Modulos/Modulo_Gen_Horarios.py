
from . import requests_api as api
from Modulos import Modulo_Profesores
from . import Modulo_Materias

lista_final_horarios = []
combo_profe_materia = {}

class Gen_Horario():

    def __init__(self, lista_materias, lista_profesores, max_secciones=30):
        
        self.max_secciones = max_secciones
        self.bloques_clases = {
            "L/M 7:00-8:30": [],
            "M/J 7:00-8:30": [],
            "L/M 8:45-10:15": [],
            "M/J 8:45-10:15": [],
            "L/M 10:30-12:00": [],
            "M/J 10:30-12:00": [],
            "L/M 12:15-1:45": [],
            "M/J 12:15-1:45": [],
            "L/M 2:00-3:30": [],
            "M/J 2:00-3:30": [],
            "L/M 3:45-5:15": [],
            "M/J 3:45-5:15": [],
            "L/M 5:30-7:00": [],
            "M/J 5:30-7:00": []
        }

        self.lista_materias_recorrer = lista_materias
        self.lista_profesores_recorrer = lista_profesores

    def __str__(self):
        return f"Información de la asignación:\n\n {self.bloques_clases}"

    
    def __repr__(self):
            return f"Materia(nombre='{self.nombre}', codigo='{self.codigo}', secciones={self.secciones})"

    def asignar_profe_materia(self):
        print(f"Materias recibidas: {len(self.lista_materias_recorrer)}")
        print(f"Profesores recibidos: {len(self.lista_profesores_recorrer)}")
        
        for materia in self.lista_materias_recorrer:
            for profesor in self.lista_profesores_recorrer:

                if (materia.codigo in profesor.materias) and (profesor.max_carga > 0):
                    
                    combo_profe_materia = {
                        "materia": materia,
                        "profesor": profesor
                    }
                    
                    self.bloques_clases["L/M 7:00-8:30"].append(combo_profe_materia)

                    profesor.max_carga -= 1
                    
                    break  
