"""
validaciones.py

Funciones de validación de datos ingresados por el usuario.
Acá vive la lógica de los dos gateways del diagrama BPMN:

  Gateway 1: ¿CUIT/CUIL válido? (formato + dígito verificador)
  Gateway 2: ¿Monto mensual estimado > $500.000?

También cubre el "camino infeliz": qué pasa si el usuario ingresa
texto donde se espera un número, o un CUIT/monto con formato inválido.
"""

from estados import LIMITE_MONTO_APROBACION_DIRECTA


def validar_cuit(cuit: str) -> bool:
    """
    Valida formato y dígito verificador de un CUIT/CUIL.

    Acepta el CUIT con o sin guiones (ej. "20-12345678-9" o "20123456789").
    Devuelve False ante cualquier entrada no numérica o de longitud incorrecta,
    sin lanzar excepciones (parte del manejo del camino infeliz).
    """
    if not isinstance(cuit, str):
        return False

    cuit_limpio = cuit.replace("-", "").strip()

    if not cuit_limpio.isdigit():
        return False

    if len(cuit_limpio) != 11:
        return False

    # Algoritmo del dígito verificador (módulo 11)
    multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    digitos = [int(d) for d in cuit_limpio]

    suma = sum(d * m for d, m in zip(digitos[:10], multiplicadores))
    resto = suma % 11
    digito_verificador_calculado = 11 - resto

    if digito_verificador_calculado == 11:
        digito_verificador_calculado = 0
    elif digito_verificador_calculado == 10:
        # Combinación inválida para CUIT/CUIL persona física estándar
        return False

    return digito_verificador_calculado == digitos[10]


def validar_rubro(rubro: str) -> bool:
    """
    Valida que el rubro ingresado no esté vacío y tenga contenido real
    (no solo espacios o caracteres sueltos).
    """
    if not isinstance(rubro, str):
        return False
    return len(rubro.strip()) >= 3


def validar_monto(monto_str: str):
    """
    Intenta convertir el monto ingresado a float.
    Devuelve (True, monto_float) si es válido, o (False, None) si no lo es.

    Cubre explícitamente el caso de "camino infeliz" que pide el enunciado:
    si se espera un número y el usuario envía texto, no debe romper el programa.
    """
    try:
        monto = float(monto_str.replace(",", "."))
        if monto <= 0:
            return False, None
        return True, monto
    except (ValueError, AttributeError):
        return False, None


def requiere_aprobacion_gerente(monto: float) -> bool:
    """
    Gateway 2: determina si el monto mensual estimado supera el límite
    que permite aprobación directa.
    """
    return monto > LIMITE_MONTO_APROBACION_DIRECTA


def validar_razon_social(razon_social: str) -> bool:
    """
    Valida que la razón social no esté vacía.
    """
    if not isinstance(razon_social, str):
        return False
    return len(razon_social.strip()) >= 2