import matplotlib.pyplot as plt

"""
En este modulo se encarga de usar la informacion de los horarios
para poder mostrar diferentes estadisticas mediante la generacion
de 3 gráficos basicos, por lo que primero se debe generar un horario
antes de poder utilizar este modulo correctamente.
"""

def grafico_salones_ocupados(horario):
    """
    Esta funcion genera un grafico de los
    salones ocupados a cada hora
    """

    horarios = list(horario.bloques_clases.keys())
    ocupacion = []
    for clases in horario.bloques_clases.values():
        ocupacion.append(len(clases))

    plt.bar(horarios, ocupacion)
    plt.title("Salones ocupados por hora")
    plt.xticks(rotation=90)
    plt.show()

def grafico_porc_maxcarga(horario):
    """
    Esta función determina qué porcentaje de la carga maxima de materias
    de cada profesor fue realmente ocupado por secciones asignadas.
    """
    nombres_profes = []
    porcentajes_profes = []

    for profe in horario.lista_profesores_recorrer:
        asignadas = 0
        for clases in horario.bloques_clases.values():
            for c in clases:
                if profe.nombre in c["profesor"]:
                    asignadas += 1
        
        total_original = asignadas + profe.max_carga
        
        if total_original > 0:
            porcentaje = (asignadas / total_original) * 100
            nombres_profes.append(profe.nombre) # Usamos solo el nombre para no saturar el texto
            porcentajes_profes.append(porcentaje)

    plt.bar(nombres_profes, porcentajes_profes)
    plt.title("% de Carga Asignada por Profesor")
    plt.show()


def grafico_porc_secciones(horario):
    """
    Esta función consolida las secciones cerradas por falta de docentes y 
    por falta de espacio físico, comparándolas con el total de secciones 
    solicitadas inicialmente.
    """
    nombres_materias = []
    porcentajes_mat = []

    for m in horario.lista_materias_recorrer:
        asignadas = 0
        for clases in horario.bloques_clases.values():
            for c in clases:
                if m.codigo in c["materia"]:
                    asignadas += 1
        
        cerradas_profe = horario.cerradas_por_profe.get(m.nombre, 0)
        cerradas_salon = horario.cerradas_por_salon.get(m.nombre, 0)
        total_cerradas = cerradas_profe + cerradas_salon
        
        total_secciones = asignadas + total_cerradas
        
        if total_secciones > 0:
            porcentaje = (total_cerradas / total_secciones) * 100
            nombres_materias.append(m.nombre)
            porcentajes_mat.append(porcentaje)

    plt.bar(nombres_materias, porcentajes_mat)
    plt.title("% de Secciones Cerradas por Materia")
    plt.xticks(rotation=90)
    plt.show()
