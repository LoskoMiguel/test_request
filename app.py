from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Configurar la ruta del archivo JSON para que funcione tanto en desarrollo como en producción
if os.environ.get('VERCEL_ENV'):
    # En Vercel, usar la carpeta /tmp
    filename = "/tmp/data.json"
else:
    # En desarrollo local, usar el directorio actual
    filename = "data.json"

# Crear el archivo JSON si no existe
def init_json():
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({"productos": []}, f)

# Cargar datos existentes
def load_data():
    init_json()
    with open(filename, 'r') as f:
        return json.load(f)

# Guardar datos
def save_data(data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        
        data = load_data()
        data["productos"].append({
            "nombre": name,
            "precio": price
        })
        save_data(data)
        return redirect(url_for('index'))
    
    data = load_data()
    return render_template('index.html', productos=data["productos"])

if __name__ == '__main__':
    app.run(debug=True)
