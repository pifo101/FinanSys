#Logica para hacer el cálculo del crédito

import math

# Calcula la cuota, interés total y total pagado
def calcular_credito(monto, tasa_mensual, plazo_meses):
    # tasa_mensual ya debe ser decimal (ej. 0.01 = 1%)
    if tasa_mensual == 0:
        cuota = monto / plazo_meses
    else:
        cuota = (monto * tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)
    total_pagado = cuota * plazo_meses
    interes_total = total_pagado - monto
    return cuota, interes_total, total_pagado

# Genera la tabla de amortización
def calcular_amortizacion(monto, tasa_mensual, plazo_meses):
    cuota = (monto * tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)
    tabla = []
    saldo = monto

    for i in range(1, plazo_meses + 1):
        interes = saldo * tasa_mensual
        capital = cuota - interes
        saldo -= capital
        tabla.append({
            "mes": i,
            "cuota": round(cuota, 2),
            "interes": round(interes, 2),
            "capital": round(capital, 2),
            "saldo": round(saldo if saldo > 0 else 0, 2)
        })

    return tabla


def calculadora_flexible(opcion, vi=None, vf=None, r=None, n=None, unidad_tasa="anual", unidad_plazo="años"):
    try:
        # --- Conversión de tasa a mensual (como base de cálculo) ---
        if unidad_tasa == "anual":
            r_decimal = (1 + r / 100) ** (1 / 12) - 1
        elif unidad_tasa == "mensual":
            r_decimal = r / 100
        elif unidad_tasa == "diaria":
            r_decimal = (1 + r / 100) ** 30 - 1
        else:
            return "Unidad de tasa no válida."

        # --- Conversión del plazo a meses ---
        if unidad_plazo == "años":
            n_meses = n * 12
        elif unidad_plazo == "meses":
            n_meses = n
        elif unidad_plazo == "días":
            n_meses = n / 30
        else:
            return "Unidad de plazo no válida."

        # --- Cálculos principales ---
        if opcion == '1':  # Monto final
            resultado = vi * ((1 + r_decimal) ** n_meses)
            texto = f"Monto final estimado: Q{resultado:.2f}"

        elif opcion == '2':  # Monto inicial
            resultado = vf / ((1 + r_decimal) ** n_meses)
            texto = f"Monto inicial necesario: Q{resultado:.2f}"

        elif opcion == '3':  # Rendimiento
            resultado = ((vf / vi) ** (1 / n_meses) - 1) * 100
            texto = f"Rendimiento necesario: {resultado:.2f}% mensual equivalente"

        elif opcion == '4':  # Tiempo
            resultado = math.log(vf / vi) / math.log(1 + r_decimal)
            texto = f"Tiempo estimado: {resultado:.2f} meses"

        else:
            texto = "Opción no válida."

        return texto

    except Exception as e:
        return "Error en el cálculo. Verifica los datos ingresados."
    
    
    

def calcular_mora(monto_base, tasa_mora, atraso, unidad_retraso, unidad_tasa, tolerancia_dias):
    try:
        # --- Convertir el atraso a días ---
        if unidad_retraso == "mes":
            atraso_dias = atraso * 30
        elif unidad_retraso == "día":
            atraso_dias = atraso
        else:
            return "Unidad de retraso no válida."

        # --- Aplicar la tolerancia (si está dentro del período de gracia, no hay mora) ---
        if atraso_dias <= tolerancia_dias:
            return "No se aplicó mora: el retraso está dentro del período de gracia."

        # --- Convertir la tasa de mora a tasa diaria ---
        if unidad_tasa == "Año(s)":
            tasa_diaria = (1 + tasa_mora / 100) ** (1 / 365) - 1
        elif unidad_tasa == "Mes(es)":
            tasa_diaria = (1 + tasa_mora / 100) ** (1 / 30) - 1
        elif unidad_tasa == "Semana(s)":
            tasa_diaria = (1 + tasa_mora / 100) ** (1 / 7) - 1
        elif unidad_tasa == "Día(s)":
            tasa_diaria = tasa_mora / 100
        else:
            return "Unidad de tasa no válida."

        # --- Calcular la mora solo por los días que superan la tolerancia ---
        dias_con_mora = atraso_dias - tolerancia_dias
        monto_total = monto_base * ((1 + tasa_diaria) ** dias_con_mora)
        mora_total = monto_total - monto_base

        # --- Resultado final ---
        texto = (
            f"Mora aplicada por {dias_con_mora} día(s) de atraso (tras {tolerancia_dias} días de gracia):\n"
            f"Tasa de mora: {tasa_mora}% {unidad_tasa.lower()}\n"
            f"Monto base: Q{monto_base:.2f}\n"
            f"Monto de mora: Q{mora_total:.2f}\n"
            f"Total a pagar con mora: Q{monto_total:.2f}"
        )

        return texto

    except Exception as e:
        return f"Error en el cálculo: {e}"