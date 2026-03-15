import csv
import json

def convert():
    try:
        # 1. Leemos el archivo físico que guardó la opción 6
        with open("profesores.json", "r", encoding="utf-8") as file:
            json_file = json.load(file)
            
        if not json_file:
            print("El archivo JSON está vacío.")
            return
            
        # 2. Sacamos los títulos de las columnas
        fieldnames = json_file[0].keys()

        # 3. Escribimos el CSV
        with open("profesores.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for data in json_file:
                writer.writerow(data)
                
        print("\n[ÉXITO] Archivo profesores.csv creado correctamente.")
        
    except FileNotFoundError:
        print("\n[!] Error: No se encontró 'profesores.json'. Corre la opción 6 primero.")
    except Exception as e:
        print(f"\n[!] Ocurrió un error al convertir: {e}")

    import csv
import json

def cargar_y_mostrar_csv():
    """Lee el horario guardado y lo imprime en consola con formato de tabla."""
    nombre_archivo = "horario_generado.csv"
    print("\n" + "="*70)
    print(" " * 20 + "CARGANDO HORARIO DESDE ARCHIVO CSV")
    print("="*70)
    
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv, delimiter=';')
            
            encabezados = next(lector)
            print(f"| {' | '.join(encabezados)} |")
            print("-" * 70)
            
            contador = 0
            for fila in lector:
                if fila:
                    print(f"| {' | '.join(fila)} |")
                    contador += 1
            
            print("-" * 70)
            print(f"\n[ÉXITO] Se visualizaron {contador} registros.")
            
    except FileNotFoundError:
        print(f"\n[!] ERROR: No se encontró '{nombre_archivo}'.")
    except PermissionError:
        print(f"\n[!] ERROR: El archivo está abierto en Excel. Ciérralo primero.")
    except Exception as e:
        print(f"\n[!] Error inesperado: {e}")