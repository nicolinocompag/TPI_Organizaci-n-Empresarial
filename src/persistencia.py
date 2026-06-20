"""
persistencia.py

Funciones de lectura y escritura de la "base de datos" simulada
(archivo CSV). No contiene lógica de negocio: solo guarda y recupera
datos del disco.

Se registran TODOS los casos (aprobado, rechazado, derivado) para
mantener trazabilidad completa del proceso, tal como ocurriría con
una base de datos real en un sistema administrativo.
"""

import csv
import os
from datetime import datetime

RUTA_ARCHIVO = os.path.join(os.path.dirname(__file__), "..", "data", "proveedores.csv")

ENCABEZADOS = [
    "id_proveedor",
    "razon_social",
    "cuit",
    "rubro",
    "monto_mensual_estimado",
    "estado",
    "fecha_alta",
]


def inicializar_csv():
    """
    Crea el archivo CSV con encabezados si todavía no existe.
    Se llama una sola vez al arrancar el programa.
    """
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(ENCABEZADOS)


def _siguiente_id() -> int:
    """
    Calcula el próximo id_proveedor en base a la cantidad de filas
    ya existentes en el CSV (encabezado no cuenta).
    """
    proveedores = leer_proveedores()
    return len(proveedores) + 1


def guardar_proveedor(razon_social: str, cuit: str, rubro: str,
                       monto: float, estado: str) -> int:
    """
    Agrega una fila nueva al CSV con los datos del proveedor y el
    estado final del proceso (APROBADO, RECHAZADO o DERIVADO).
    Devuelve el id_proveedor asignado.
    """
    inicializar_csv()
    id_proveedor = _siguiente_id()
    fecha_alta = datetime.now().strftime("%Y-%m-%d %H:%M")

    fila = [id_proveedor, razon_social, cuit, rubro, monto, estado, fecha_alta]

    with open(RUTA_ARCHIVO, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fila)

    return id_proveedor


def leer_proveedores() -> list:
    """
    Devuelve todas las filas de proveedores registradas (sin el
    encabezado). Si el archivo no existe todavía, devuelve lista vacía.
    """
    if not os.path.exists(RUTA_ARCHIVO):
        return []

    with open(RUTA_ARCHIVO, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        filas = list(reader)

    if not filas:
        return []

    return filas[1:]  # se descarta el encabezado


def existe_proveedor(cuit: str) -> bool:
    """
    Chequea si un CUIT ya fue registrado previamente, para evitar
    altas duplicadas.
    """
    proveedores = leer_proveedores()
    cuit_limpio = cuit.replace("-", "").strip()
    return any(fila[2] == cuit_limpio for fila in proveedores if len(fila) > 2)