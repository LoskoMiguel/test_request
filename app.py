from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Configurar la ruta del archivo JSON
filename = os.path.join(os.getcwd(), "data.json")

# Crear el archivo JSON si no existe
if not os.path.exists(filename):
    with open(filename, 'w') as f:
        json.dump({"productos": []}, f)

# Cargar datos existentes
def load_data():
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {"productos": []}

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

# Esto es para desarrollo local
if __name__ == '__main__':
    app.run(debug=True)
