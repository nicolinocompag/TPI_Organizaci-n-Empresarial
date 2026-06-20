"""
estados.py

Define los estados posibles de la máquina de estados del proceso
de Alta de Proveedores. Cada estado representa un nodo del diagrama
BPMN (to-be).

Se usan constantes de texto (strings) en lugar de una clase Enum,
para mantener el código alineado con los temas vistos en la cursada.
Cada constante es simplemente una variable que guarda un string fijo;
usarlas en vez de escribir el texto "a mano" en cada lugar del código
evita errores de tipeo (ej. escribir "Inicio" en un lado e "INICIO"
en otro), sin necesidad de definir una clase.
"""

# --- Estados del proceso (cada uno es un string constante) ---
INICIO = "INICIO"
INGRESO_RAZON_SOCIAL = "INGRESO_RAZON_SOCIAL"
INGRESO_CUIT = "INGRESO_CUIT"
VALIDANDO_CUIT = "VALIDANDO_CUIT"
DERIVADO = "DERIVADO"                                   # CUIT inválido tras 3 intentos
INGRESO_RUBRO = "INGRESO_RUBRO"
INGRESO_MONTO = "INGRESO_MONTO"
VALIDANDO_MONTO = "VALIDANDO_MONTO"
APROBACION_DIRECTA = "APROBACION_DIRECTA"               # monto <= 500K
PENDIENTE_APROBACION_GERENTE = "PENDIENTE_APROBACION_GERENTE"  # monto > 500K
APROBADO = "APROBADO"                                   # gerente aprobó
RECHAZADO = "RECHAZADO"                                 # gerente rechazó
REGISTRO_BASE_DATOS = "REGISTRO_BASE_DATOS"
FIN = "FIN"

# Límite de reintentos para la validación de CUIT (gateway 1)
MAX_INTENTOS_CUIT = 3

# Monto límite (en pesos) que define el gateway 2 (riesgo/aprobación)
LIMITE_MONTO_APROBACION_DIRECTA = 500000