"""
Módulo de Sincronización con API de GitHub

Este módulo se encarga de realizar las peticiones HTTP para descargar los 
datos más recientes de profesores y materias, asegurando que el sistema 
trabaje con información actualizada.
"""

import requests
import json

# URLs de los archivos crudos (raw) en el repositorio de GitHub
profesores_url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/profesores.json"
materias_url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json"

def descargar():
    """
    Descarga los datos de la API y los guarda en archivos JSON locales.
    """
    # Con este try-except buscamos evitar que el programa se cuelgue por un error de conexión o de red, 
    # ya que alguien puede no tener internet, estar detrás de un firewall o el servidor de GitHub 
    # podría estar caído temporalmente.
    try:
        # 1. Descargamos y guardamos las materias
        print("Sincronizando materias con la nube...")
        response_materias = requests.get(materias_url)
        
        if response_materias.status_code == 200:
            # Guardamos con el nombre exacto que espera el Modulo_Materias
            with open("materias2526-1.json", "w", encoding="utf-8") as file:
                json.dump(response_materias.json(), file, indent=4, ensure_ascii=False)
            print(" -> [OK] Materias actualizadas.")
        else:
            print(f" -> [!] Fallo en materias. Código de estado: {response_materias.status_code}")

        # 2. Descargamos y guardamos los profesores
        print("Sincronizando profesores con la nube...")
        response_profesores = requests.get(profesores_url)
        
        if response_profesores.status_code == 200:
            with open("profesores.json", "w", encoding="utf-8") as file:
                json.dump(response_profesores.json(), file, indent=4, ensure_ascii=False)
            print(" -> [OK] Profesores actualizados.")
        else:
            print(f" -> [!] Fallo en profesores. Código de estado: {response_profesores.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n[!] Error de conexión: No se pudo establecer comunicación con GitHub.")
        print("Verifique su conexión a internet.")
    except Exception as e:
        print(f"\n[!] Ocurrió un error inesperado durante la descarga: {e}")