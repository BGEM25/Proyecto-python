from Modulos import Modulo_Profesores
from Modulos import Modulo_Materias
from Modulos import requests_api
from Modulos.Modulo_Gen_Horarios import Gen_Horario
import json
# z = 0
# for profe in Modulo_Profesores.crear_objeto_fromapi():
#     z += 1
#     print(f"{z}",profe)
        
# print(Modulo_Profesores.specific_profesor())

# 11671718
# 11593482

# 1. Pedimos el dato físico de los salones
salones_disponibles = int(input("Ingrese el numero de salones disponibles por bloque: "))

# 2. Instanciamos el objeto
mi_horario = Gen_Horario(
    Modulo_Materias.lista_final_materias, 
    Modulo_Profesores.lista_final_profesor, 
    salones_disponibles
)

# 3. Ejecutamos la lógica de asignación
mi_horario.asignar_profe_materia()

# 4. Imprimimos el JSON para que sigas viendo la estructura interna
print("\n" + "="*50)
print("          HORARIO EN JSON")
print("="*50)
print(json.dumps(mi_horario.bloques_clases, indent=2, ensure_ascii=False))

# 5. ¡AQUÍ LLAMAMOS AL NUEVO REPORTE AUTOMÁTICO!
mi_horario.generar_reporte()