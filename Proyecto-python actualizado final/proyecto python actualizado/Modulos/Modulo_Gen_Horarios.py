"""
Módulo de Generación de Horarios

Este módulo contiene la lógica del algoritmo de asignación. Se encarga de
distribuir las materias entre los profesores disponibles, validando choques
de horario y disponibilidad de salones físicos.
"""

from . import requests_api as api
from Modulos import Modulo_Profesores
from . import Modulo_Materias

lista_final_horarios = []
combo_profe_materia = {}

class Horario():
    """
    Clase principal para la creación y gestión de la malla horaria.
    """

    def __init__(self, max_secciones):
        """
        Prepara la estructura de bloques y mapea los profesores por materia.
        
        Consideraciones de eficiencia:
        - Tiempo: O(P * K), donde P son los profesores y K sus materias asociadas.
        - Memoria: O(M), donde M son los códigos de las materias en el diccionario 
          'profes_por_materia' para búsquedas en tiempo O(1).
        """
        self.max_secciones = max_secciones
        self.bloques_clases = {
            "L/M 7:00-8:30": [], "M/J 7:00-8:30": [],
            "L/M 8:45-10:15": [], "M/J 8:45-10:15": [],
            "L/M 10:30-12:00": [], "M/J 10:30-12:00": [],
            "L/M 12:15-1:45": [], "M/J 12:15-1:45": [],
            "L/M 2:00-3:30": [], "M/J 2:00-3:30": [],
            "L/M 3:45-5:15": [], "M/J 3:45-5:15": [],
            "L/M 5:30-7:00": [], "M/J 5:30-7:00": []
        }

        self.lista_materias_recorrer = Modulo_Materias.lista_final_materias
        self.lista_profesores_recorrer = Modulo_Profesores.lista_final_profesor

        self.cerradas_por_profe = {}
        self.cerradas_por_salon = {}
        self.profes_por_materia = {}

        # Mapeo: Organizamos qué profesores pueden dictar cada código de materia
        for profe in self.lista_profesores_recorrer:
            for mat in profe.materias:
                if mat not in self.profes_por_materia:
                    self.profes_por_materia[mat] = []
                self.profes_por_materia[mat].append(profe)

    def hay_espacio_en_bloque(self, horario_actual):
        """
        Comprueba si el límite de salones por bloque ha sido alcanzado.
        Eficiencia: O(1) tiempo, ya que la función len() en diccionarios de Python
        retorna la cuenta guardada en memoria instantáneamente.
        """
        return len(self.bloques_clases[horario_actual]) < self.max_secciones

    def profesor_disponible_en_bloque(self, horario_actual, profesor):
        """
        Verifica que un profesor no tenga otra clase asignada a la misma hora.
        Eficiencia: O(S), donde 'S' es max_secciones. Como S es constante (ej. 30), 
        se considera O(1) acotado.
        """
        for clase in self.bloques_clases[horario_actual]:
            if profesor.nombre in clase["profesor"] and profesor.apellido in clase["profesor"]:
                return False
        return True

    def materia_repetida_en_bloque(self, horario_actual, materia):
        """
        Verifica si la materia ya existe en este bloque para evitar redundancia.
        Eficiencia: O(S) acotado a O(1) en tiempo.
        """
        for clase in self.bloques_clases[horario_actual]:
            if materia.codigo in clase["materia"]:
                return True
        return False

    def generar_y_reportar(self):
        """
        Ejecuta el algoritmo de asignación y muestra el reporte de resultados.
        Eficiencia: Delegada a los métodos principales llamados.
        """
        self.asignar_profe_materia()
        self.generar_reporte()

    def procesar_asignacion(self, horario_actual, combo, profesor, materia):
        """
        Registra la clase y descuenta la carga disponible del docente y la materia.
        Eficiencia: O(1) tiempo y espacio, usando inserción (append) en lista.
        """
        self.bloques_clases[horario_actual].append(combo)
        profesor.max_carga -= 1
        materia.secciones -= 1

    def avanzar_indice(self, indice_horario, total_bloques):
        """
        Incrementa el puntero de horario de forma circular.
        Eficiencia: O(1) operaciones aritméticas básicas.
        """
        indice_horario += 1
        return 0 if indice_horario >= total_bloques else indice_horario

    def buscar_espacio(self, materia, profesor, nombres_horarios, total_bloques, indice_horario, plan_b):
        """
        Busca un bloque disponible que cumpla con las restricciones de salón y profesor.
        Eficiencia: O(B * S), donde B son los bloques (14) y S las secciones máximas.
        Al estar acotado por un límite fijo de salones y bloques, es O(1) analítico.
        """
        intentos_bloque = 0
        while intentos_bloque < total_bloques:
            horario_actual = nombres_horarios[indice_horario]
            espacio = self.hay_espacio_en_bloque(horario_actual)
            profe_libre = self.profesor_disponible_en_bloque(horario_actual, profesor)
            
            if plan_b:
                condicion = espacio and profe_libre
            else:
                mat_repetida = self.materia_repetida_en_bloque(horario_actual, materia)
                condicion = espacio and profe_libre and not mat_repetida
                
            if condicion:
                return horario_actual, indice_horario
                
            indice_horario = self.avanzar_indice(indice_horario, total_bloques)
            intentos_bloque += 1
        return None, indice_horario

    def intentar_reasignacion(self, materia_actual, nombres_horarios, total_bloques):
        """
        Algoritmo de reasignación (swap) que libera a un profesor ocupado 
        moviendo sus clases actuales a otros docentes libres.
        
        Consideraciones de eficiencia:
        - Tiempo: O(P * B * S * K), donde P=profesores, B=bloques, S=salones, K=materias.
          Debido a la naturaleza fuertemente acotada de las restricciones del mundo real 
          (max bloques = 14, max carga = 4), se considera de profundidad limitada.
        """
        if materia_actual.codigo not in self.profes_por_materia:
            return False
            
        for profe_ocupado in self.profes_por_materia[materia_actual.codigo]:
            if profe_ocupado.max_carga == 0:
                for horario in nombres_horarios:
                    for clase in self.bloques_clases[horario]:
                        if profe_ocupado.nombre in clase["profesor"] and profe_ocupado.apellido in clase["profesor"]:
                            for codigo_viejo in profe_ocupado.materias:
                                if codigo_viejo in clase["materia"] and codigo_viejo in self.profes_por_materia:
                                    for profe_libre in self.profes_por_materia[codigo_viejo]:
                                        if profe_libre != profe_ocupado and profe_libre.max_carga > 0 and self.profesor_disponible_en_bloque(horario, profe_libre):
                                            profe_ocupado.max_carga += 1
                                            horario_elegido, _ = self.buscar_espacio(materia_actual, profe_ocupado, nombres_horarios, total_bloques, 0, False)
                                            if not horario_elegido:
                                                horario_elegido, _ = self.buscar_espacio(materia_actual, profe_ocupado, nombres_horarios, total_bloques, 0, True)
                                                
                                            if horario_elegido:
                                                clase["profesor"] = f"{profe_libre.nombre} {profe_libre.apellido}"
                                                profe_libre.max_carga -= 1
                                                combo_nuevo = {
                                                     "materia": f" Imparte: {materia_actual.nombre} \n Codigo materia: {materia_actual.codigo}",
                                                     "profesor": f"{profe_ocupado.nombre} {profe_ocupado.apellido}"
                                                }
                                                self.procesar_asignacion(horario_elegido, combo_nuevo, profe_ocupado, materia_actual)
                                                return True
                                            profe_ocupado.max_carga -= 1
        return False

    def asignar_profe_materia(self):
        """
        Bucle principal de asignación que recorre todas las materias y secciones.
        
        Consideraciones de eficiencia:
        - Tiempo: Complejidad combinada del algoritmo O(M * P * B * S), pero 
          optimizado mediante la indexación del diccionario en O(1).
        """
        nombres_horarios = list(self.bloques_clases.keys())
        total_bloques = len(nombres_horarios)
        indice_horario = 0

        for materia in self.lista_materias_recorrer:
            if materia.codigo not in self.profes_por_materia:
                if materia.nombre not in self.cerradas_por_profe:
                    self.cerradas_por_profe[materia.nombre] = 0
                self.cerradas_por_profe[materia.nombre] += materia.secciones
                materia.secciones = 0
                continue
                
            while materia.secciones > 0:
                seccion_asignada = False
                for profesor in self.profes_por_materia[materia.codigo]:
                    if profesor.max_carga > 0:
                        combo_dict = {
                             "materia": f" Imparte: {materia.nombre} \n Codigo materia: {materia.codigo}",
                             "profesor": f"{profesor.nombre} {profesor.apellido}"
                        }
                        horario_elegido, indice_horario = self.buscar_espacio(materia, profesor, nombres_horarios, total_bloques, indice_horario, False)
                        if not horario_elegido:
                            horario_elegido, indice_horario = self.buscar_espacio(materia, profesor, nombres_horarios, total_bloques, indice_horario, True)
                            
                        if horario_elegido:
                            self.procesar_asignacion(horario_elegido, combo_dict, profesor, materia)
                            indice_horario = self.avanzar_indice(indice_horario, total_bloques)
                            seccion_asignada = True
                            break
                            
                if not seccion_asignada:
                    exito = self.intentar_reasignacion(materia, nombres_horarios, total_bloques)
                    if not exito:
                        horas_disponibles = sum(p.max_carga for p in self.profes_por_materia[materia.codigo])
                        if horas_disponibles == 0:
                            self.cerradas_por_profe[materia.nombre] = self.cerradas_por_profe.get(materia.nombre, 0) + 1
                        else:
                            self.cerradas_por_salon[materia.nombre] = self.cerradas_por_salon.get(materia.nombre, 0) + 1
                        materia.secciones -= 1

    def generar_reporte(self):
        """
        Imprime un resumen detallado de la asignación de la sesión.
        Eficiencia: Tiempo O(B * S) al recorrer los diccionarios. Memoria O(1).
        """
        print("\n" + "="*50)
        print("          REPORTE DE ASIGNACIÓN")
        print("="*50)
        print("\n1. SECCIONES CERRADAS POR FALTA DE PROFESORES:")
        if not self.cerradas_por_profe: print("   - Ninguna.")
        else:
            for n, c in self.cerradas_por_profe.items(): print(f"   - {n}: {c} sección(es) cerrada(s).")
        print("\n2. SECCIONES NO ASIGNADAS POR FALTA DE SALONES:")
        if not self.cerradas_por_salon: print("   - Ninguna.")
        else:
            for n, c in self.cerradas_por_salon.items(): print(f"   - {n}: {c} sección(es) sin asignar.")
        print("\n3. HORARIOS CON SALONES DISPONIBLES:")
        for h, clases in self.bloques_clases.items():
            libres = self.max_secciones - len(clases)
            if libres > 0: print(f"   - {h}: {libres} salón(es) libre(s).")
        print("="*50 + "\n")

    def buscar_horario_materia(self, busqueda):
        """
        Filtra los bloques para mostrar el horario de una materia.
        Eficiencia: Tiempo O(B * S) por iteración total.
        """
        encontrado = False
        for h, clases in self.bloques_clases.items():
            for c in clases:
                if busqueda.lower() in c["materia"].lower():
                    print(f"[{h}] -> Profesor: {c['profesor']}")
                    encontrado = True
        if not encontrado: print("No se encontraron clases para esa materia.")

    def buscar_horario_profesor(self, busqueda):
        """
        Filtra los bloques para mostrar el horario de un profesor.
        Eficiencia: Tiempo O(B * S) por iteración total sobre la malla.
        """
        encontrado = False
        for h, clases in self.bloques_clases.items():
            for c in clases:
                if busqueda.lower() in c["profesor"].lower():
                    m_limpia = c["materia"].replace("\n", " | ")
                    print(f"[{h}] -> {m_limpia}")
                    encontrado = True
        if not encontrado: print("No se encontró ese profesor.")

    def ver_salones_hora(self, bloque_buscado):
        """
        Muestra el detalle de ocupación de un bloque horario específico.
        Eficiencia: Tiempo O(B + S).
        """
        encontrado = False
        for h, clases in self.bloques_clases.items():
            if bloque_buscado.lower() in h.lower():
                print(f"\n--- {h} ---\nSalones en uso: {len(clases)} | Libres: {self.max_secciones - len(clases)}")
                for c in clases:
                    m_limpia = c["materia"].replace("\n", " ")
                    print(f"  - {m_limpia} | Prof: {c['profesor']}")
                encontrado = True
        if not encontrado: print("Bloque no encontrado.")

    def exportar_csv(self):
        """
        Exporta la malla horaria a un archivo CSV persistente.
        Eficiencia: Tiempo O(B * S). Memoria O(1) por escritura contigua.
        """
        try:
            archivo = open("horario_generado.csv", "w", encoding="utf-8")
            archivo.write("Bloque Horario,Materia,Profesor\n")
            for h, clases in self.bloques_clases.items():
                for c in clases:
                    m_limpia = c["materia"].replace("\n", " | ")
                    archivo.write(f"{h},{m_limpia},{c['profesor']}\n")
            archivo.close()
            print("\n[ÉXITO] Horario guardado en 'horario_generado.csv'.")
        except PermissionError:
            print("\n[!] ERROR: No se puede guardar. Cierre el archivo en Excel e intente de nuevo.")
        except Exception as e:
            print(f"\n[!] Error inesperado al exportar: {e}")

    def obtener_secciones(self, busqueda):
        """
        Retorna una lista de secciones que coincidan con el nombre de la materia.
        Eficiencia: Tiempo O(B * S). Memoria O(K) donde K son los hallazgos.
        """
        secciones = []
        for h, clases in self.bloques_clases.items():
            for i, c in enumerate(clases):
                if busqueda.lower() in c["materia"].lower():
                    secciones.append({"horario": h, "indice": i, "datos": c})
        return secciones

    def obtener_profesores_libres(self, codigo_mat, horario_evaluar, profe_actual_nombre):
        """
        Encuentra docentes calificados que tengan carga disponible a una hora dada.
        Eficiencia: Tiempo O(P), dependiente de la cantidad total de profesores 
        calificados para la materia consultada.
        """
        disponibles = []
        for p in self.profes_por_materia.get(codigo_mat, []):
            if f"{p.nombre} {p.apellido}" == profe_actual_nombre:
                if self.profesor_disponible_en_bloque(horario_evaluar, p): disponibles.append(p)
            elif p.max_carga > 0 and self.profesor_disponible_en_bloque(horario_evaluar, p):
                disponibles.append(p)
        return disponibles

    def aplicar_modificacion(self, horario_viejo, indice, horario_nuevo, profe_nuevo, profe_viejo_nombre):
        """
        Efectúa el cambio manual de una sección actualizando la carga docente.
        Eficiencia: Tiempo O(P) para actualizar la carga del profesor saliente, 
        y O(S) para el pop de la lista del bloque horario. Memoria O(1).
        """
        clase_a_mover = self.bloques_clases[horario_viejo].pop(indice)
        for p in self.lista_profesores_recorrer:
            if f"{p.nombre} {p.apellido}" == profe_viejo_nombre:
                p.max_carga += 1
                break
        profe_nuevo.max_carga -= 1
        clase_a_mover["profesor"] = f"{profe_nuevo.nombre} {profe_nuevo.apellido}"
        self.bloques_clases[horario_nuevo].append(clase_a_mover)