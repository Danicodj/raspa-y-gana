from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import os

app = Flask(__name__, static_url_path='/static')

JUGADAS_FILE = 'jugadas.json'

# Cargar historial si existe
if os.path.exists(JUGADAS_FILE):
    with open(JUGADAS_FILE, 'r') as f:
        jugadas = json.load(f)
else:
    jugadas = {}

@app.route('/')
def index():
    return render_template('juego.html')

@app.route('/api/jugar', methods=['POST'])
def jugar():
    data = request.get_json()
    codigo = data.get('codigo', '').strip()

    if not codigo:
        return jsonify({"status": "error", "mensaje": "Debes ingresar un código válido."}), 400

    if codigo in jugadas:
        return jsonify({"status": "bloqueado", "mensaje": "Este código ya ha sido usado."})

    # Lógica simple para premios
    premio = "🎫 Gracias por participar"
    if datetime.now().second % 5 == 0:
        premio = "🎉 ¡Ganaste un premio especial!"

    # Guardar jugada
    jugadas[codigo] = {
        "fecha": datetime.now().isoformat(),
        "premio": premio
    }

    with open(JUGADAS_FILE, 'w') as f:
        json.dump(jugadas, f, indent=2)

    return jsonify({"status": "ok", "premio": premio})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
