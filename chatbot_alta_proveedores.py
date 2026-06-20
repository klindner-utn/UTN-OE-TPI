"""
Simulador de Chatbot - Alta de Proveedores
TPI - Organización Empresarial
TUPAD - UTN
"""

import csv
import re
import os
from datetime import datetime

ARCHIVO_CSV = "proveedores.csv"
CAMPOS = ["razon_social", "cuit", "rubro", "email", "telefono", "condicion_fiscal", "estado", "fecha_alta", "solicitante"]

# Utilizamos archivo CSV como BD

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CAMPOS).writeheader()

def leer_proveedores():
    with open(ARCHIVO_CSV, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def guardar_proveedor(datos):
    with open(ARCHIVO_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CAMPOS).writerow(datos)

def proveedor_existe(cuit):
    return any(p["cuit"] == cuit for p in leer_proveedores())

# Validaciones con regex

def validar_cuit(cuit):
    return bool(re.match(r"^\d{2}-\d{8}-\d{1}$", cuit))

def validar_email(email):
    return bool(re.match(r"^[\w.+-]+@[\w-]+\.\w+$", email))

# Interfaz

def bot_msg(texto):
    print(f"\nBot: {texto}")

def usuario_input(prompt="Vos: "):
    return input(f"\n{prompt}").strip()

# Proceso de alta

def proceso_alta():
    bot_msg("Hola! Soy el asistente de Alta de Proveedores de KenTech S.R.L.")
    bot_msg("Escribi /cancelar en cualquier momento para abortar")

    # Razon social
    bot_msg("Ingresa la RAZON SOCIAL del proveedor:")
    razon_social = usuario_input()
    if razon_social.lower() == "/cancelar":
        bot_msg("Proceso cancelado")
        return

    # CUIT con validacion
    while True:
        bot_msg("Ingresa el CUIT (formato XX-XXXXXXXX-X):")
        cuit = usuario_input()
        if cuit.lower() == "/cancelar":
            bot_msg("Proceso cancelado")
            return
        if validar_cuit(cuit):
            break
        bot_msg("CUIT invalido. Formato: XX-XXXXXXXX-X (ej: 30-12345678-9)")

    # Verificar duplicado
    if proveedor_existe(cuit):
        bot_msg(f"El proveedor con CUIT {cuit} ya esta registrado")
        return

    # Rubro
    rubros = {"1": "Tecnologia", "2": "Logistica", "3": "Servicios", "4": "Otro"}
    while True:
        bot_msg("Selecciona el RUBRO:\n   1) Tecnologia  2) Logistica  3) Servicios  4) Otro")
        op = usuario_input()
        if op.lower() == "/cancelar":
            bot_msg("Proceso cancelado")
            return
        if op in rubros:
            rubro = rubros[op]
            break
        bot_msg("Opcion invalida. Ingresa 1, 2, 3 o 4")

    # Email
    while True:
        bot_msg("Ingresa el EMAIL de contacto:")
        email = usuario_input()
        if email.lower() == "/cancelar":
            bot_msg("Proceso cancelado")
            return
        if validar_email(email):
            break
        bot_msg("Email invalido (ej: contacto@empresa.com)")

    # Telefono
    bot_msg("Ingresa el TELEFONO de contacto:")
    telefono = usuario_input()
    if telefono.lower() == "/cancelar":
        bot_msg("Proceso cancelado")
        return

    # Condicion fiscal
    condiciones = {"1": "Responsable Inscripto", "2": "Monotributista", "3": "Exento"}
    while True:
        bot_msg("CONDICION FISCAL ante AFIP:\n   1) Responsable Inscripto  2) Monotributista  3) Exento")
        op = usuario_input()
        if op.lower() == "/cancelar":
            bot_msg("Proceso cancelado")
            return
        if op in condiciones:
            condicion_fiscal = condiciones[op]
            break
        bot_msg("Opcion invalida. Ingresa 1, 2 o 3")

    # Resumen
    bot_msg("RESUMEN:")
    print(f"   Razon Social:     {razon_social}")
    print(f"   CUIT:             {cuit}")
    print(f"   Rubro:            {rubro}")
    print(f"   Email:            {email}")
    print(f"   Telefono:         {telefono}")
    print(f"   Condicion Fiscal: {condicion_fiscal}")

    # Compuerta - condicion fiscal
    if condicion_fiscal == "Responsable Inscripto":
        bot_msg("Resp. Inscripto -> Aprobación automatica")
        estado = "Aprobado"
    else:
        bot_msg(f"{condicion_fiscal} -> Requiere aprobacion del Jefe de Compras")
        bot_msg("--- [Simulacion: Jefe de Compras] ---")
        while True:
            bot_msg("Aprueba el alta? (si/no)")
            decision = usuario_input("Jefe: ").lower()
            if decision in ("si", "sí", "s"):
                estado = "Aprobado"
                bot_msg("Jefe APROBO el alta")
                break
            elif decision in ("no", "n"):
                bot_msg("Jefe RECHAZO el alta. Proveedor NO registrado")
                return
            bot_msg("Ingresa 'si' o 'no'")

    # Guardar datos
    guardar_proveedor({
        "razon_social": razon_social, "cuit": cuit, "rubro": rubro,
        "email": email, "telefono": telefono, "condicion_fiscal": condicion_fiscal,
        "estado": estado, "fecha_alta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "solicitante": "usuario_compras"
    })
    bot_msg(f"Proveedor '{razon_social}' registrado exitosamente!")

def listar_proveedores():
    proveedores = leer_proveedores()
    if not proveedores:
        bot_msg("No hay proveedores registrados")
        return
    bot_msg(f"Proveedores registrados ({len(proveedores)}):\n")
    print(f"  {'Razon Social':<22} {'CUIT':<15} {'Rubro':<12} {'Cond. Fiscal':<20} {'Estado':<10} {'Fecha'}")
    print("   " + "-" * 90)
    for p in proveedores:
        print(f"   {p['razon_social']:<22} {p['cuit']:<15} {p['rubro']:<12} {p['condicion_fiscal']:<20} {p['estado']:<10} {p['fecha_alta']}")

# Main - Cuerpo principal

def main():
    inicializar_csv()
    print("=" * 55)
    print("  KenTech S.R.L. - Alta de Proveedores (Chatbot)")
    print("=" * 55)

    while True:
        print("\n" + "-" * 40)
        print("Indicame que operacion queres realizar:")
        print("\n  /alta   -> Iniciar alta de proveedor")
        print("  /listar -> Ver proveedores registrados")
        print("  /salir  -> Cerrar")
        print("-" * 40)
        cmd = usuario_input("Comando: ").lower()

        if cmd == "/alta":
            proceso_alta()
        elif cmd == "/listar":
            listar_proveedores()
        elif cmd == "/salir":
            bot_msg("Hasta luego!")
            break
        else:
            bot_msg("Comando no reconocido. Podes usar /alta, /listar o /salir")

if __name__ == "__main__":
    main()
