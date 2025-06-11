from flask import Flask, render_template, request, jsonify
from escacs import inicialitzar_partida, moviment_valid, fer_moviment, obtenir_estat

app = Flask(__name__)
partida = inicialitzar_partida()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/moviment', methods=['POST'])
def moviment():
    dades = request.get_json()
    origen = dades['origen']
    desti = dades['desti']
    
    if moviment_valid(partida, origen, desti):
        fer_moviment(partida, origen, desti)
        return jsonify({"status": "ok", "tauler": obtenir_estat(partida)})
    else:
        return jsonify({"status": "invalid"})

@app.route('/estat')
def estat():
    return jsonify(obtenir_estat(partida))

if __name__ == '__main__':
    app.run(debug=True)
