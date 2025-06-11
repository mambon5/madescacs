PIECES = {
    "blanca": {"peon": "♙", "torre": "♖", "alfil": "♗", "caball": "♘", "rei": "♔", "reina": "♕"},
    "negra": {"peon": "♟", "torre": "♜", "alfil": "♝", "caball": "♞", "rei": "♚", "reina": "♛"},
}

def inicialitzar_partida():
    peces = ["torre", "caball", "alfil", "reina", "rei", "alfil", "caball", "torre"]
    tauler = [["" for _ in range(8)] for _ in range(8)]
    for i in range(8):
        tauler[0][i] = PIECES["negra"][peces[i]]
        tauler[1][i] = PIECES["negra"]["peon"]
        tauler[6][i] = PIECES["blanca"]["peon"]
        tauler[7][i] = PIECES["blanca"][peces[i]]
    return {"tauler": tauler, "torn": "blanca"}

def obtenir_estat(partida):
    return {"tauler": partida["tauler"], "torn": partida["torn"]}

def moviment_valid(partida, ori, dest):
    y1, x1 = ori['y'], ori['x']
    y2, x2 = dest['y'], dest['x']
    tauler = partida["tauler"]
    peça = tauler[y1][x1]

    if peça == "":
        return False

    color = "blanca" if peça in PIECES["blanca"].values() else "negra"
    if color != partida["torn"]:
        return False

    # No es permet moviment a la mateixa posició
    if (y1, x1) == (y2, x2):
        return False

    # Només es permet moviment a casella buida o enemic (simplificat)
    desti = tauler[y2][x2]
    if desti and (desti in PIECES[color].values()):
        return False

    # Aquesta validació és molt bàsica, per a practicar
    return True

def fer_moviment(partida, ori, dest):
    y1, x1 = ori['y'], ori['x']
    y2, x2 = dest['y'], dest['x']
    tauler = partida["tauler"]
    tauler[y2][x2] = tauler[y1][x1]
    tauler[y1][x1] = ""
    partida["torn"] = "negra" if partida["torn"] == "blanca" else "blanca"
