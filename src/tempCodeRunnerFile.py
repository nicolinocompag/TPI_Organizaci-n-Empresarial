"""
main.py

Punto de entrada del bot de Alta de Proveedores.
Implementa la máquina de estados que recorre el flujo definido en
el diagrama BPMN (to-be), conectando validaciones.py y persistencia.py.

La máquina de estados se implementa con un bucle while y comparaciones
de strings (variable estado_actual), sin usar clases ni Enum.

Ejecutar con:
    python src/main.py
"""

import estados
from validaciones import (
    validar_cuit,
    validar_rubro,
    validar_monto,
    validar_razon_social,
    requiere_aprobacion_gerente,
)
from persistencia import guardar_proveedor, existe_proveedor


def main():
    estado_actual = estados.INICIO

    # Datos que se van completando a lo largo de la conversación
    razon_social = None
    cuit = None
    rubro = None
    monto = None
    intentos_cuit = 0

    while estado_actual != estados.FIN:

        # ----------------------------------------------------------
        if estado_actual == estados.INICIO:
            print("=" * 50)
            print("BOT DE ALTA DE PROVEEDORES")
            print("=" * 50)
            print("Iniciamos el proceso de alta. Escribí 'salir' en")
            print("cualquier momento para cancelar.\n")
            estado_actual = estados.INGRESO_RAZON_SOCIAL

        # ----------------------------------------------------------
        elif estado_actual == estados.INGRESO_RAZON_SOCIAL:
            entrada = input("Ingrese razón social: ").strip()
            if entrada.lower() == "salir":
                print("\nProceso cancelado por el usuario.")
                estado_actual = estados.FIN
                continue

            if not validar_razon_social(entrada):
                print(" -> Razón social inválida (mínimo 2 caracteres). Intente de nuevo.\n")
                continue

            razon_social = entrada.strip()
            estado_actual = estados.INGRESO_CUIT

        # ----------------------------------------------------------
        elif estado_actual == estados.INGRESO_CUIT:
            entrada = input("Ingrese CUIT/CUIL (formato: 20-12345678-6): ").strip()
            if entrada.lower() == "salir":
                print("\nProceso cancelado por el usuario.")
                estado_actual = estados.FIN
                continue

            cuit = entrada
            estado_actual = estados.VALIDANDO_CUIT

        # ----------------------------------------------------------
        elif estado_actual == estados.VALIDANDO_CUIT:
            if validar_cuit(cuit):
                if existe_proveedor(cuit):
                    print(" -> Este CUIT ya se encuentra registrado como proveedor.\n")
                    estado_actual = estados.DERIVADO
                    continue
                intentos_cuit = 0  # reset para futuras validaciones
                estado_actual = estados.INGRESO_RUBRO
            else:
                intentos_cuit += 1
                restantes = estados.MAX_INTENTOS_CUIT - intentos_cuit
                if restantes > 0:
                    print(f" -> CUIT inválido. Le quedan {restantes} intento(s).\n")
                    estado_actual = estados.INGRESO_CUIT
                else:
                    print(" -> Intentos agotados. Se deriva el caso al Departamento de Compras.\n")
                    estado_actual = estados.DERIVADO

        # ----------------------------------------------------------
        elif estado_actual == estados.DERIVADO:
            guardar_proveedor(razon_social or "N/D", cuit or "N/D",
                               rubro or "N/D", monto or 0, "DERIVADO")
            print("Se envió un e-mail al Departamento de Compras para reconctacto manual.")
            estado_actual = estados.FIN

        # ----------------------------------------------------------
        elif estado_actual == estados.INGRESO_RUBRO:
            entrada = input("Ingrese rubro del proveedor: ").strip()
            if entrada.lower() == "salir":
                print("\nProceso cancelado por el usuario.")
                estado_actual = estados.FIN
                continue

            if not validar_rubro(entrada):
                print(" -> Rubro inválido (mínimo 3 caracteres). Intente de nuevo.\n")
                continue

            rubro = entrada
            estado_actual = estados.INGRESO_MONTO

        # ----------------------------------------------------------
        elif estado_actual == estados.INGRESO_MONTO:
            entrada = input("Ingrese monto mensual estimado de operación ($): ").strip()
            if entrada.lower() == "salir":
                print("\nProceso cancelado por el usuario.")
                estado_actual = estados.FIN
                continue

            es_valido, valor = validar_monto(entrada)
            if not es_valido:
                print(" -> Monto inválido. Ingrese solo números (ej: 350000).\n")
                continue

            monto = valor
            estado_actual = estados.VALIDANDO_MONTO

        # ----------------------------------------------------------
        elif estado_actual == estados.VALIDANDO_MONTO:
            if requiere_aprobacion_gerente(monto):
                print(f" -> Monto (${monto:,.2f}) supera el límite de aprobación directa.\n")
                estado_actual = estados.PENDIENTE_APROBACION_GERENTE
            else:
                print(f" -> Monto (${monto:,.2f}) dentro del límite. Aprobación directa.\n")
                estado_actual = estados.APROBACION_DIRECTA

        # ----------------------------------------------------------
        elif estado_actual == estados.APROBACION_DIRECTA:
            estado_actual = estados.APROBADO

        # ----------------------------------------------------------
        elif estado_actual == estados.PENDIENTE_APROBACION_GERENTE:
            print("El caso queda pendiente de aprobación del Gerente.")
            respuesta = input("[Simulación] Gerente, ¿aprueba el alta? (S/N): ").strip().upper()
            if respuesta == "S":
                estado_actual = estados.APROBADO
            else:
                estado_actual = estados.RECHAZADO

        # ----------------------------------------------------------
        elif estado_actual == estados.APROBADO:
            id_asignado = guardar_proveedor(razon_social, cuit, rubro, monto, "APROBADO")
            print(f"\n✔ Proveedor APROBADO y registrado con ID {id_asignado}.")
            estado_actual = estados.FIN

        # ----------------------------------------------------------
        elif estado_actual == estados.RECHAZADO:
            id_asignado = guardar_proveedor(razon_social, cuit, rubro, monto, "RECHAZADO")
            print(f"\n✘ Proveedor RECHAZADO por el Gerente. Registrado con ID {id_asignado}.")
            estado_actual = estados.FIN

    # ----------------------------------------------------------
    print("\nProceso de alta finalizado. Gracias por utilizar el sistema.")


if __name__ == "__main__":
    main()