import requests
import json

profesores_url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/profesores.json"
materias_url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json"

def descargar():
    """Descarga los datos de la API y los guarda en archivos JSON locales."""
    try:
        # 1. Descargamos y guardamos las materias
        print("Descargando materias desde Github...")
        response_materias = requests.get(materias_url)
        
        if response_materias.status_code == 200:
            with open("materias.json", "w", encoding="utf-8") as file:
                json.dump(response_materias.json(), file, indent=4, ensure_ascii=False)
            print(" -> Materias actualizadas correctamente.")
        else:
            print(f" -> Error al descargar materias. Código: {response_materias.status_code}")

        # 2. Descargamos y guardamos los profesores
        print("Descargando profesores desde Github...")
        response_profesores = requests.get(profesores_url)
        
        if response_profesores.status_code == 200:
            with open("profesores.json", "w", encoding="utf-8") as file:
                json.dump(response_profesores.json(), file, indent=4, ensure_ascii=False)
            print(" -> Profesores actualizados correctamente.")
        else:
            print(f" -> Error al descargar profesores. Código: {response_profesores.status_code}")

    except Exception as e:
        print(f"\n[!] Ocurrió un error de conexión: {e}")
