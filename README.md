# FinanSys

Calculadora financiera web hecha con Flask. Incluye herramientas para amortización de créditos, cálculo flexible de intereses y cálculo de mora.

## Funcionalidades

- Calculadora de amortización con tabla mensual.
- Calculadora flexible para monto inicial, monto final, rendimiento o tiempo.
- Calculadora de mora con período de gracia.
- Páginas informativas sobre el proyecto.

## Requisitos

- Python 3.10 o superior.
- pip.

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/pifo101/FinanSys.git
cd FinanSys
```

Crea un entorno virtual:

```bash
python -m venv .venv
```

Activa el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Inicia la aplicación:

```bash
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:5000
```

## Estructura

- `app.py`: rutas principales de Flask.
- `logica.py`: cálculos financieros.
- `templates/`: páginas HTML.
- `static/`: estilos e imágenes.
- `requirements.txt`: dependencias del proyecto.
