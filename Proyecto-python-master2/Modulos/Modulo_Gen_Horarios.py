from . import requests_api as api
from Modulos import Modulo_Profesores
from . import Modulo_Materias

lista_final_horarios = []
combo_profe_materia = {}

class Gen_Horario():

    def __init__(self, lista_materias, lista_profesores, max_secciones):
        
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

        self.cerradas_por_profe = {}
        self.cerradas_por_salon = {}
        self.profes_por_materia = {}

        for profe in self.lista_profesores_recorrer:
            for mat in profe.materias:
                if mat not in self.profes_por_materia:
                    self.profes_por_materia[mat] = []
                self.profes_por_materia[mat].append(profe)

    def __str__(self):
        return f"Información de la asignación:\n\n {self.bloques_clases}"
    
    def hay_espacio_en_bloque(self, horario_actual):
        if len(self.bloques_clases[horario_actual]) < self.max_secciones:
            return True
        return False

    def profesor_disponible_en_bloque(self, horario_actual, profesor):
        for clase in self.bloques_clases[horario_actual]:
            if profesor.nombre in clase["profesor"] and profesor.apellido in clase["profesor"]:
                return False
        return True

    def materia_repetida_en_bloque(self, horario_actual, materia):
        for clase in self.bloques_clases[horario_actual]:
            if materia.codigo in clase["materia"]:
                return True
        return False

    def procesar_asignacion(self, horario_actual, combo, profesor, materia):
        self.bloques_clases[horario_actual].append(combo)
        profesor.max_carga -= 1
        materia.secciones -= 1

    def avanzar_indice(self, indice_horario, total_bloques):
        indice_horario += 1
        if indice_horario >= total_bloques:
            return 0
        return indice_horario

    def buscar_espacio(self, materia, profesor, nombres_horarios, total_bloques, indice_horario, plan_b):
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
                        combo_profe_materia = {
                             "materia": f" Imparte: {materia.nombre} \n Codigo materia: {materia.codigo}",
                             "profesor": f"{profesor.nombre} {profesor.apellido}"
                        }
                        
                        horario_elegido, indice_horario = self.buscar_espacio(
                            materia, profesor, nombres_horarios, total_bloques, indice_horario, False
                        )
                        
                        if not horario_elegido:
                            horario_elegido, indice_horario = self.buscar_espacio(
                                materia, profesor, nombres_horarios, total_bloques, indice_horario, True
                            )
                            
                        if horario_elegido:
                            self.procesar_asignacion(horario_elegido, combo_profe_materia, profesor, materia)
                            indice_horario = self.avanzar_indice(indice_horario, total_bloques)
                            seccion_asignada = True
                            break
                            
                if not seccion_asignada:
                    exito = self.intentar_reasignacion(materia, nombres_horarios, total_bloques)
                    
                    if not exito:
                        horas_disponibles = 0
                        for p in self.profes_por_materia[materia.codigo]:
                            horas_disponibles += p.max_carga
                            
                        if horas_disponibles == 0:
                            if materia.nombre not in self.cerradas_por_profe:
                                self.cerradas_por_profe[materia.nombre] = 0
                            self.cerradas_por_profe[materia.nombre] += 1
                        else:
                            if materia.nombre not in self.cerradas_por_salon:
                                self.cerradas_por_salon[materia.nombre] = 0
                            self.cerradas_por_salon[materia.nombre] += 1
                            
                        materia.secciones -= 1

    def generar_reporte(self):
        print("\n" + "="*50)
        print("          REPORTE DE ASIGNACIÓN")
        print("="*50)
        
        print("\n1. SECCIONES CERRADAS POR FALTA DE PROFESORES:")
        if not self.cerradas_por_profe:
            print("   - Ninguna.")
        else:
            for nombre, cantidad in self.cerradas_por_profe.items():
                print(f"   - {nombre}: {cantidad} sección(es) cerrada(s).")
                
        print("\n2. SECCIONES NO ASIGNADAS POR FALTA DE SALONES:")
        if not self.cerradas_por_salon:
            print("   - Ninguna.")
        else:
            for nombre, cantidad in self.cerradas_por_salon.items():
                print(f"   - {nombre}: {cantidad} sección(es) sin asignar.")
                
        print("\n3. HORARIOS CON SALONES DISPONIBLES:")
        hay_espacio = False
        for horario, clases in self.bloques_clases.items():
            espacio_sobrante = self.max_secciones - len(clases)
            if espacio_sobrante > 0:
                print(f"   - {horario}: {espacio_sobrante} salón(es) libre(s).")
                hay_espacio = True
                
        if not hay_espacio:
            print("   - Ningún horario tiene salones disponibles.")
            
        print("="*50 + "\n")


    def buscar_horario_materia(self, busqueda):
        encontrado = False
        for horario, clases in self.bloques_clases.items():
            for clase in clases:
                if busqueda.lower() in clase["materia"].lower():
                    print(f"[{horario}] -> Profesor: {clase['profesor']}")
                    encontrado = True
        if not encontrado:
            print("No se encontraron clases asignadas para esa materia.")

    def buscar_horario_profesor(self, busqueda):
        encontrado = False
        for horario, clases in self.bloques_clases.items():
            for clase in clases:
                if busqueda.lower() in clase["profesor"].lower():
                    materia_limpia = clase["materia"].replace("\n", " | ")
                    print(f"[{horario}] -> {materia_limpia}")
                    encontrado = True
        if not encontrado:
            print("No se encontraron clases asignadas para este profesor.")

    def ver_salones_hora(self, bloque_buscado):
        encontrado = False
        for horario, clases in self.bloques_clases.items():
            if bloque_buscado.lower() in horario.lower():
                usados = len(clases)
                libres = self.max_secciones - usados
                print(f"\n--- {horario} ---")
                print(f"Salones en uso: {usados} | Salones libres: {libres}")
                for clase in clases:
                    materia_limpia = clase["materia"].replace("\n", " ")
                    print(f"  - {materia_limpia} | Prof: {clase['profesor']}")
                encontrado = True
        if not encontrado:
            print("Bloque de horario no encontrado.")

    def exportar_csv(self):
        archivo = open("horario_generado.csv", "w", encoding="utf-8")
        
        archivo.write("Bloque Horario,Materia,Profesor\n")
        
        for horario, clases in self.bloques_clases.items():
            for clase in clases:
       
                materia_limpia = clase["materia"].replace("\n", " | ")
                profesor = clase["profesor"]
                
                archivo.write(f"{horario},{materia_limpia},{profesor}\n")
                
        archivo.close()
        print("\n[ÉXITO] El horario ha sido guardado en el archivo 'horario_generado.csv'.")
        print("Puedes abrirlo directamente con Excel o cualquier hoja de cálculo.")

    def obtener_secciones(self, busqueda):
        """Devuelve una lista con los datos exactos de las secciones encontradas."""
        secciones = []
        for horario, clases in self.bloques_clases.items():
            for indice, clase in enumerate(clases):
                if busqueda.lower() in clase["materia"].lower():
                    secciones.append({"horario": horario, "indice": indice, "datos": clase})
        return secciones

    def obtener_profesores_libres(self, codigo_mat, horario_evaluar, profe_actual_nombre):
        """Devuelve una lista de los profesores que pueden dar la clase a una hora específica."""
        disponibles = []
        for p in self.profes_por_materia.get(codigo_mat, []):
            # Si es el profe actual, solo validamos que no choque en la nueva hora
            if f"{p.nombre} {p.apellido}" == profe_actual_nombre:
                if self.profesor_disponible_en_bloque(horario_evaluar, p):
                    disponibles.append(p)
            # Si es un profe distinto, validamos que tenga horas libres y no choque
            elif p.max_carga > 0 and self.profesor_disponible_en_bloque(horario_evaluar, p):
                disponibles.append(p)
        return disponibles

    def aplicar_modificacion(self, horario_viejo, indice, horario_nuevo, profe_nuevo, profe_viejo_nombre):
        """Ejecuta el cambio físico en el diccionario y ajusta las horas de los profesores."""
        clase_a_mover = self.bloques_clases[horario_viejo].pop(indice)
        
        # Devolvemos la hora al profe viejo
        for p in self.lista_profesores_recorrer:
            if f"{p.nombre} {p.apellido}" == profe_viejo_nombre:
                p.max_carga += 1
                break
                
        # Le quitamos la hora al nuevo y actualizamos el nombre
        profe_nuevo.max_carga -= 1
        clase_a_mover["profesor"] = f"{profe_nuevo.nombre} {profe_nuevo.apellido}"
        
        # Metemos la clase en su destino final
        self.bloques_clases[horario_nuevo].append(clase_a_mover)