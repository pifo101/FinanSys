from flask import Flask, render_template, request
from logica import calcular_credito, calcular_amortizacion, calculadora_flexible, calcular_mora
app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    resumen = None
    tabla = []
    error = None

    if request.method == "POST":
        try:
            monto = float(request.form["monto"])
            tasa = float(request.form["tasa"])
            unidad_tasa = request.form["unidad_tasa"]
            plazo = float(request.form["plazo"])
            unidad_plazo = request.form["unidad_plazo"]

            if monto <= 0:
                raise ValueError("El monto debe ser mayor a cero.")
            if tasa < 0:
                raise ValueError("La tasa no puede ser negativa.")
            if plazo <= 0:
                raise ValueError("El plazo debe ser mayor a cero.")

            if unidad_tasa == "anual":
                tasa_mensual = (1 + tasa / 100) ** (1 / 12) - 1
            elif unidad_tasa == "mensual":
                tasa_mensual = tasa / 100
            elif unidad_tasa == "diaria":
                tasa_mensual = (1 + tasa / 100) ** 30 - 1
            else:
                raise ValueError("Unidad de tasa no válida.")

            if unidad_plazo == "años":
                plazo_meses = int(plazo * 12)
            elif unidad_plazo == "meses":
                plazo_meses = int(plazo)
            elif unidad_plazo == "días":
                plazo_meses = int(plazo / 30)
            else:
                raise ValueError("Unidad de plazo no válida.")

            if plazo_meses <= 0:
                raise ValueError("El plazo debe equivaler al menos a 1 mes.")

            cuota, interes_total, total_pagado = calcular_credito(monto, tasa_mensual, plazo_meses)
            tabla = calcular_amortizacion(monto, tasa_mensual, plazo_meses)
            resumen = {
                "monto": monto,
                "tasa": tasa,
                "unidad_tasa": unidad_tasa,
                "plazo": plazo,
                "unidad_plazo": unidad_plazo,
                "cuota": cuota,
                "interes_total": interes_total,
                "total_pagado": total_pagado,
            }
        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Error en los datos ingresados."

    return render_template("calculadora.html", resumen=resumen, tabla=tabla, error=error)

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

            if opcion not in ['1', '2', '3', '4']:
                raise ValueError("Selecciona el tipo de cálculo.")
            if unidad_tasa not in ["anual", "mensual", "diaria"]:
                raise ValueError("Unidad de tasa no válida.")
            if unidad_plazo not in ["años", "meses", "días"]:
                raise ValueError("Unidad de plazo no válida.")

            vi = float(vi) if vi not in (None, "") else None
            vf = float(vf) if vf not in (None, "") else None
            r = float(r) if r not in (None, "") else None
            n = float(n) if n not in (None, "") else None

            if opcion == '1' and (vi is None or r is None or n is None):
                raise ValueError("Ingresa monto inicial, rendimiento y plazo.")
            if opcion == '2' and (vf is None or r is None or n is None):
                raise ValueError("Ingresa monto final, rendimiento y plazo.")
            if opcion == '3' and (vi is None or vf is None or n is None):
                raise ValueError("Ingresa monto inicial, monto final y plazo.")
            if opcion == '4' and (vi is None or vf is None or r is None):
                raise ValueError("Ingresa monto inicial, monto final y rendimiento.")

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
        except ValueError as e:
            error = str(e)
        except Exception:
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




@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

if __name__ == "__main__":
    app.run(debug=True)
