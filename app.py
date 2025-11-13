from flask import Flask, render_template, request
from logica import calcular_credito, calcular_amortizacion, calculadora_flexible, calcular_mora
app = Flask(__name__)

# Renderizar Página principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Renderizar calculadora flexible

@app.route("/Cal_flex")
def Call_cal_flex():
    return render_template("Cal_flex.html")

# Renderizar calculadora de amortización

@app.route("/calculadora")
def Call_calculadora():
    return render_template("calculadora.html")

# Renderizar calculadora de mora

@app.route("/Cal_mora")
def Call_mora():
    return render_template("mora.html")


# Renderizar página acerca de

@app.route("/acerca")
def Call_acerca():
    return render_template("acerca.html")


@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    resultado = ""

    if request.method == "POST":
        monto = float(request.form["monto"])
        tasa = float(request.form["tasa"])
        unidad_tasa = request.form["unidad_tasa"]
        plazo = float(request.form["plazo"])
        unidad_plazo = request.form["unidad_plazo"]

        # Convertimos la tasa a decimal mensual
        if unidad_tasa == "anual":
            tasa_mensual = (1 + tasa / 100) ** (1 / 12) - 1
        elif unidad_tasa == "mensual":
            tasa_mensual = tasa / 100
        elif unidad_tasa == "diaria":
            tasa_mensual = (1 + tasa / 100) ** 30 - 1

        # Convertimos el plazo a meses
        if unidad_plazo == "años":
            plazo_meses = int(plazo * 12)
        elif unidad_plazo == "meses":
            plazo_meses = int(plazo)
        elif unidad_plazo == "días":
            plazo_meses = int(plazo / 30)

        # Calculamos cuota y tabla
        cuota, interes_total, total_pagado = calcular_credito(monto, tasa_mensual, plazo_meses)
        tabla = calcular_amortizacion(monto, tasa_mensual, plazo_meses)

        # Construimos el resultado en texto
        resultado += "--------------------------------------------------\n\n"
        resultado += "Datos ingresados\n"
        resultado += f"Monto: Q{monto:.2f}\n"
        resultado += f"Tasa: {tasa}% ({unidad_tasa})\n"
        resultado += f"Plazo: {plazo} {unidad_plazo}\n\n"

        resultado += "--------------------------------------------------\n\n"
        resultado += "Datos obtenidos\n"
        resultado += f"Cuota mensual: Q{cuota:.2f}\n"
        resultado += f"Interés total: Q{interes_total:.2f}\n"
        resultado += f"Total pagado: Q{total_pagado:.2f}\n\n"
        resultado += "Tabla de amortización:\n"
        resultado += "Mes   Cuota      Interés    Capital    Saldo\n"
        resultado += "--------------------------------------------------\n"

        for fila in tabla:
            resultado += f"{fila['mes']:2}   {fila['cuota']:8.2f}   {fila['interes']:8.2f}   {fila['capital']:8.2f}   {fila['saldo']:10.2f}\n"

    return render_template("calculadora.html", resultado=resultado)

@app.route('/Cal_flex', methods=['GET', 'POST'])
def Cal_flex():
    resultado = None
    error = None

    if request.method == 'POST':
        try:
            opcion = request.form.get('opcion')
            vi = request.form.get('vi')
            vf = request.form.get('vf')
            r = request.form.get('r')
            n = request.form.get('n')
            unidad_tasa = request.form.get('unidad_tasa')
            unidad_plazo = request.form.get('unidad_plazo')

            # convertir sólo a float o None, SIN transformar unidades aquí
            vi = float(vi) if vi not in (None, "") else None
            vf = float(vf) if vf not in (None, "") else None
            r = float(r) if r not in (None, "") else None    # r queda en PORCENTAJE (ej. 12)
            n = float(n) if n not in (None, "") else None    # n queda en la unidad que eligió el usuario

            # Llamada segura pasando argumentos por nombre
            resultado = calculadora_flexible(
                opcion,
                vi=vi,
                vf=vf,
                r=r,
                n=n,
                unidad_tasa=unidad_tasa,
                unidad_plazo=unidad_plazo
            )

            if not resultado:
                error = "Verifica los valores ingresados."
        except Exception as e:
            # opcional: print(e) para debug en consola
            # print("Error Cal_flex:", e)
            error = "Error en los datos."

    return render_template('Cal_flex.html', resultado=resultado, error=error)




@app.route('/Cal_mora', methods=['GET', 'POST'])
def Cal_mora():
    resultado = None

    if request.method == 'POST':
        try:
            monto_base = float(request.form['monto'])
            tasa_mora = float(request.form['tasa'])
            atraso = float(request.form['atraso'])
            unidad_tasa = request.form['unidad']
            unidad_retraso = request.form['unidad_retraso']
            tolerancia_dias = float(request.form['tolerancia'])

            resultado = calcular_mora(
                monto_base, tasa_mora, atraso, unidad_retraso, unidad_tasa, tolerancia_dias
            )

        except Exception as e:
            resultado = f"Error en los datos: {e}"

    return render_template('mora.html', resultado=resultado)




# Página "Acerca de"
@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

if __name__ == "__main__":
    app.run(debug=True)