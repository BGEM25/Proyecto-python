from Modulos import Modulo_Profesores
from Modulos import Modulo_Materias
from Modulos import requests_api

# z = 0
# for profe in Modulo_Profesores.crear_objeto_fromapi():
#     z += 1
#     print(f"{z}",profe)
        
# print(Modulo_Profesores.specific_profesor())

# 11671718
# 11593482



profes_llenos = Modulo_Profesores.lista_final_profesor
materias_llenas = Modulo_Materias.lista_final_materias

mi_horario = Modulo_Gen_Horarios.Gen_Horario(materias_llenas, profes_llenos)

mi_horario.asignar_profe_materia()
print(mi_horario)