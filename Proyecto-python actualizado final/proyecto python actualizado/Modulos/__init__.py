"""
Configuración del paquete de Módulos.

Este archivo permite que Python reconozca la carpeta como un paquete y 
define cuáles de sus módulos internos serán accesibles de forma pública 
cuando se utilice la importación masiva, o sea, el *.

Consideraciones de eficiencia:
- Tiempo y Memoria: O(1), ya que es únicamente una definición estática 
  de una estructura de datos (lista de strings) en tiempo de compilación.
"""

__all__ = [
    "Modulo_Materias",
    "Modulo_Profesores",
    "Modulo_Gen_Horarios",
    "Modulo_Mod_Horarios",
    "Modulo_Estadisticas",
    "json_to_csv",
    "requests_api"
]