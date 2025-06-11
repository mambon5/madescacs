import tkinter as tk
import time

TAM_CASILLA = 80
TIEMPO_INICIAL = 10 * 60  # 10 minuts en segons

PIEZAS = {
    "blancas": {"torre": "♖", "caballo": "♘", "alfil": "♗", "reina": "♕", "rey": "♔", "peon": "♙"},
    "negras": {"torre": "♜", "caballo": "♞", "alfil": "♝", "reina": "♛", "rey": "♚", "peon": "♟"}
}
movimientos_rey = {"blanca": False, "negra": False}
movimientos_torre = {
    "blanca": {"izq": False, "der": False},
    "negra": {"izq": False, "der": False}
}



tablero = [["" for _ in range(8)] for _ in range(8)]
turno = "blanca"
pieza_seleccionada = None
origen = None
movimientos_validos = []
rey_jaque_pos = None
heart_item = None
heart_scale = 1.0
heart_direction = 1

tiempo_restante = {"blanca": TIEMPO_INICIAL, "negra": TIEMPO_INICIAL}
ultimo_update = time.time()
juego_activo = True

def inicializar_tablero():
    piezas = ["torre", "caballo", "alfil", "reina", "rey", "alfil", "caballo", "torre"]
    for i in range(8):
        tablero[0][i] = PIEZAS["negras"][piezas[i]]
        tablero[1][i] = PIEZAS["negras"]["peon"]
        tablero[6][i] = PIEZAS["blancas"]["peon"]
        tablero[7][i] = PIEZAS["blancas"][piezas[i]]

def obtener_color(pieza):
    if pieza in PIEZAS["blancas"].values():
        return "blanca"
    elif pieza in PIEZAS["negras"].values():
        return "negra"
    return None

def es_valido(pieza, ori, dest):
    fx, cx = ori
    fy, cy = dest
    if not (0 <= fx < 8 and 0 <= cx < 8 and 0 <= fy < 8 and 0 <= cy < 8):
        return False
    dx, dy = fy - fx, cy - cx
    abs_dx, abs_dy = abs(dx), abs(dy)
    color = obtener_color(pieza)
    enemigo = "negra" if color == "blanca" else "blanca"
    destino = tablero[fy][cy]
    if destino and obtener_color(destino) == color:
        return False
    es_captura = destino and obtener_color(destino) == enemigo

    def limpio():
        pasos = max(abs_dx, abs_dy)
        paso_x = dx // pasos if dx != 0 else 0
        paso_y = dy // pasos if dy != 0 else 0
        for i in range(1, pasos):
            x = fx + i * paso_x
            y = cx + i * paso_y
            if tablero[x][y] != "":
                return False
        return True

    piezas_color = PIEZAS[color + "s"]

    if pieza == piezas_color["peon"]:
        dir = -1 if color == "blanca" else 1
        inicio = 6 if color == "blanca" else 1
        if dx == dir and dy == 0 and destino == "":
            return True
        if fx == inicio and dx == 2 * dir and dy == 0 and tablero[fx + dir][cx] == "" and destino == "":
            return True
        if dx == dir and abs_dy == 1 and es_captura:
            return True
    elif pieza == piezas_color["torre"]:
        if (dx == 0 or dy == 0) and limpio():
            return True
    elif pieza == piezas_color["alfil"]:
        if abs_dx == abs_dy and limpio():
            return True
    elif pieza == piezas_color["reina"]:
        if (abs_dx == abs_dy or dx == 0 or dy == 0) and limpio():
            return True
    elif pieza == piezas_color["rey"]:
        # Enroc
        if not movimientos_rey[color] and dx == 0 and abs(dy) == 2:
            fila_rey = fx
            # Enroc corto
            if dy == 2 and not movimientos_torre[color]["der"]:
                if tablero[fx][cx+1] == "" and tablero[fx][cx+2] == "":
                    if not rey_en_jaque(color) and \
                       not casilla_en_jaque(color, (fx, cx+1)) and \
                       not casilla_en_jaque(color, (fx, cx+2)):
                        return True
            # Enroc largo
            if dy == -2 and not movimientos_torre[color]["izq"]:
                if tablero[fx][cx-1] == "" and tablero[fx][cx-2] == "" and tablero[fx][cx-3] == "":
                    if not rey_en_jaque(color) and \
                       not casilla_en_jaque(color, (fx, cx-1)) and \
                       not casilla_en_jaque(color, (fx, cx-2)):
                        return True
        # Moviment normal del rei
        if abs_dx <= 1 and abs_dy <= 1:
            return True

    elif pieza == piezas_color["caballo"]:
        if (abs_dx, abs_dy) in [(2, 1), (1, 2)]:
            return True
    return False

def obtener_movimientos_validos(pieza, ori):
    movimientos = []
    for i in range(8):
        for j in range(8):
            if es_valido(pieza, ori, (i, j)) and movimiento_saca_jaque(pieza, ori, (i, j)):
                movimientos.append((i, j))
    return movimientos

def casilla_en_jaque(color, pos):
    enemigo = "blanca" if color == "negra" else "negra"
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza and obtener_color(pieza) == enemigo:
                if es_valido(pieza, (fila, col), pos):
                    return True
    return False


def buscar_rey(color):
    rey = PIEZAS[color + "s"]["rey"]
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] == rey:
                return (fila, col)
    return None

def rey_en_jaque(color_rey):
    pos_rey = buscar_rey(color_rey)
    if not pos_rey:
        return False
    enemigo = "blanca" if color_rey == "negra" else "negra"
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza and obtener_color(pieza) == enemigo:
                if es_valido(pieza, (fila, col), pos_rey):
                    return True
    return False

def movimiento_saca_jaque(pieza, ori, dest):
    ox, oy = ori
    dx, dy = dest
    pieza_destino = tablero[dx][dy]
    tablero[ox][oy] = ""
    tablero[dx][dy] = pieza
    resultado = not rey_en_jaque(obtener_color(pieza))
    tablero[ox][oy] = pieza
    tablero[dx][dy] = pieza_destino
    return resultado

def dibujar_tablero():
    canvas.delete("all")
    color_claro = "#f0d9b5"
    color_oscuro = "#b58863"
    for fila in range(8):
        for col in range(8):
            x1 = col * TAM_CASILLA
            y1 = fila * TAM_CASILLA
            color = color_claro if (fila + col) % 2 == 0 else color_oscuro
            canvas.create_rectangle(x1, y1, x1 + TAM_CASILLA, y1 + TAM_CASILLA, fill=color, outline="")

            if origen == (fila, col):
                canvas.create_rectangle(x1, y1, x1 + TAM_CASILLA, y1 + TAM_CASILLA, outline="red", width=4)

            if (fila, col) in movimientos_validos:
                canvas.create_oval(x1+30, y1+30, x1+50, y1+50, fill="yellow", outline="gold")

            pieza = tablero[fila][col]
            if pieza:
                fill = "white" if obtener_color(pieza) == "blanca" else "black"
                canvas.create_text(x1 + TAM_CASILLA // 2, y1 + TAM_CASILLA // 2,
                                   text=pieza, font=("Helvetica", 44), fill=fill)

    mostrar_tiempo()

def animar_corazon():
    global heart_scale, heart_direction, heart_item

    if heart_item:
        canvas.delete(heart_item)

    if rey_jaque_pos:
        fila, col = rey_jaque_pos
        x = col * TAM_CASILLA + TAM_CASILLA // 2
        y = fila * TAM_CASILLA + TAM_CASILLA // 2 - 30
        size = int(14 + 6 * heart_scale)
        heart_item = canvas.create_text(x, y, text="❤️", font=("Helvetica", size))
        heart_scale += 0.1 * heart_direction
        if heart_scale > 1.3 or heart_scale < 0.7:
            heart_direction *= -1

    canvas.after(100, animar_corazon)

def sonido_jugada():
    pass

def click(event):
    global pieza_seleccionada, origen, turno, movimientos_validos, rey_jaque_pos, ultimo_update, juego_activo

    if not juego_activo:
        return

    col = event.x // TAM_CASILLA
    fila = event.y // TAM_CASILLA

    if not (0 <= fila < 8 and 0 <= col < 8):
        return

    if pieza_seleccionada is None:
        pieza = tablero[fila][col]
        if pieza and obtener_color(pieza) == turno:
            pieza_seleccionada = pieza
            origen = (fila, col)
            movimientos_validos = obtener_movimientos_validos(pieza, origen)
    else:
        destino = (fila, col)
        if destino in movimientos_validos:
            if rey_en_jaque(turno) and not movimiento_saca_jaque(pieza_seleccionada, origen, destino):
                pieza_seleccionada = None
                origen = None
                movimientos_validos = []
                dibujar_tablero()
                canvas.create_text(8*TAM_CASILLA//2, 20,
                                   text="¡Debes salir del JAQUE!", font=("Helvetica", 20, "bold"), fill="orange")
                return

            ox, oy = origen
            dx, dy = destino
            pieza_capturada = tablero[dx][dy]
            tablero[ox][oy] = ""
            tablero[fila][col] = pieza_seleccionada
            sonido_jugada()

            if pieza_capturada in [PIEZAS["blancas"]["rey"], PIEZAS["negras"]["rey"]]:
                dibujar_tablero()
                ganador = "Negras" if turno == "blanca" else "Blancas"
                canvas.unbind("<Button-1>")
                canvas.create_text(8*TAM_CASILLA//2, 8*TAM_CASILLA//2,
                                   text=f"¡{ganador} ganen!", font=("Helvetica", 32, "bold"), fill="red")
                juego_activo = False
                return
            
            
            # Enroc
            if pieza_seleccionada == PIEZAS["blancas"]["rey"] and origen == (7, 4):
                if destino == (7, 6):  # Enroc corto blancas
                    tablero[7][5] = tablero[7][7]
                    tablero[7][7] = ""
                elif destino == (7, 2):  # Enroc largo blancas
                    tablero[7][3] = tablero[7][0]
                    tablero[7][0] = ""
                movimientos_rey["blanca"] = True
            elif pieza_seleccionada == PIEZAS["negras"]["rey"] and origen == (0, 4):
                if destino == (0, 6):  # Enroc corto negras
                    tablero[0][5] = tablero[0][7]
                    tablero[0][7] = ""
                elif destino == (0, 2):  # Enroc largo negras
                    tablero[0][3] = tablero[0][0]
                    tablero[0][0] = ""
                movimientos_rey["negra"] = True

            # Marcar moviment de rei i torre
            if pieza_seleccionada in [PIEZAS["blancas"]["rey"], PIEZAS["negras"]["rey"]]:
                movimientos_rey[turno] = True
            if pieza_seleccionada in [PIEZAS["blancas"]["torre"], PIEZAS["negras"]["torre"]]:
                if origen[1] == 0:
                    movimientos_torre[turno]["izq"] = True
                elif origen[1] == 7:
                    movimientos_torre[turno]["der"] = True

            tablero[ox][oy] = ""
            tablero[dx][dy] = pieza_seleccionada

            turno = "negra" if turno == "blanca" else "blanca"
            ultimo_update = time.time()-5

            if rey_en_jaque(turno):
                canvas.create_text(8*TAM_CASILLA//2, 20,
                                   text=f"¡JAQUE a les {turno}s!", font=("Helvetica", 24, "bold"), fill="red")
                rey_jaque_pos = buscar_rey(turno)
            else:
                rey_jaque_pos = None

        pieza_seleccionada = None
        origen = None
        movimientos_validos = []

    dibujar_tablero()

def mostrar_tiempo():
    canvas.delete("tiempo")

    minutos_b = int(tiempo_restante["blanca"] // 60)
    segons_b = int(tiempo_restante["blanca"] % 60)
    tiempo_b = f"{minutos_b:02d}:{segons_b:02d}"

    minutos_n = int(tiempo_restante["negra"] // 60)
    segons_n = int(tiempo_restante["negra"] % 60)
    tiempo_n = f"{minutos_n:02d}:{segons_n:02d}"

    canvas.create_text(8*TAM_CASILLA + 70, 100, text="Blanques", fill="black", font=("Helvetica", 12, "bold"), tags="tiempo")
    canvas.create_text(8*TAM_CASILLA + 70, 130, text=tiempo_b, fill="blue", font=("Helvetica", 16), tags="tiempo")

    canvas.create_text(8*TAM_CASILLA + 70, 180, text="Negres", fill="black", font=("Helvetica", 12, "bold"), tags="tiempo")
    canvas.create_text(8*TAM_CASILLA + 70, 210, text=tiempo_n, fill="blue", font=("Helvetica", 16), tags="tiempo")

def actualizar_tiempo():
    global ultimo_update, tiempo_restante, turno, juego_activo

    if not juego_activo:
        return

    ahora = time.time()
    elapsed = ahora - ultimo_update
    ultimo_update = ahora

    tiempo_restante[turno] -= elapsed

    if tiempo_restante[turno] <= 0:
        tiempo_restante[turno] = 0
        juego_activo = False
        ganador = "Negras" if turno == "blanca" else "Blancas"
        canvas.create_text(8*TAM_CASILLA//2, 8*TAM_CASILLA//2,
                           text=f"Temps esgotat!\n¡{ganador} guanyen!", font=("Helvetica", 32, "bold"), fill="red")
        canvas.unbind("<Button-1>")
        return

    mostrar_tiempo()
    ventana.after(1000, actualizar_tiempo)

# Iniciar finestra
ventana = tk.Tk()
ventana.title("Ajedrez amb temporitzador")
canvas = tk.Canvas(ventana, width=8*TAM_CASILLA + 140, height=8*TAM_CASILLA)
canvas.pack()
canvas.bind("<Button-1>", click)

inicializar_tablero()
dibujar_tablero()
animar_corazon()
mostrar_tiempo()
actualizar_tiempo()

ventana.mainloop()
