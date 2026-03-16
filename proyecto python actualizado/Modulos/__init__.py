"""
Configuración del paquete de Módulos.

Este archivo permite que Python reconozca la carpeta como un paquete y 
define cuáles de sus módulos internos serán accesibles de forma pública 
cuando se utilice la importación masiva, o sea, el *.
"""

__all__ = [
    "json_to_csv",
    "Modulo_Materias",
    "Modulo_Profesores",
    "requests_api",
    "Modulo_Gen_Horarios",
    "Modulo_Mod_Horarios",
    "json_to_csv",
    "requests_api"
]