from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["playing"] = True
        session["moves"] = []
    
    return render_template("game.html", game=session["board"], turn=session["turn"], playing=session["playing"], moves=session["moves"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["moves"].append((row, col, session["turn"]))

    game = session["board"]

    if game[row][0] == game[row][1] == game[row][2] or game[0][col] == game[1][col] == game[2][col] or checkDiagonals(game):
        session["playing"] = False
    elif session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/undo")
def undo():
    undoMove(session["moves"].pop())
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()     
    return redirect(url_for("index"))

@app.route("/computer")
def computer():
    move = minimax(session["board"], session["turn"])[1]
    print move
    return redirect(url_for('play', row=move[0], col=move[1]))


def checkDiagonals(game):
    if game[1][1]:
        return game[0][0] == game[1][1] == game[2][2] or game[2][0] == game[1][1] == game[0][2]
    return False

def undoMove(move):
    session["board"][move[0]][move[1]] = None
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

def minimax(game, turn):
    if game[0][0] == game[0][1] == game[0][2] == "X" or game[1][0] == game[1][1] == game[1][2] == "X" or game[2][0] == game[2][1] == game[2][2] == "X" or game[0][0] == game[1][0] == game[2][0] == "X" or game[0][1] == game[1][1] == game[2][1] == "X" or game[0][2] == game[1][2] == game[2][2] == "X" or game[0][0] == game[1][1] == game[2][2] == "X" or game[0][2] == game[1][1] == game[2][0] == "X":
        return (11, (None, None))
    elif game[0][0] == game[0][1] == game[0][2] == "O" or game[1][0] == game[1][1] == game[1][2] == "O" or game[2][0] == game[2][1] == game[2][2] == "O" or game[0][0] == game[1][0] == game[2][0] == "O" or game[0][1] == game[1][1] == game[2][1] == "O" or game[0][2] == game[1][2] == game[2][2] == "O" or game[0][0] == game[1][1] == game[2][2] == "O" or game[0][2] == game[1][1] == game[2][0] == "O":
        return (-11, (None, None))
    elif game[0][0] and game[1][0] and game[2][0] and game[0][1] and game[1][1] and game[2][1] and game[0][2] and game[1][2] and game[2][2]:
        return (0, (None, None))  
    
    moves = []
    bestmove = (None, None)
    for row in range(3):
        for col in range(3):
            if not game[row][col]:
                moves.append((row, col))
    
    if turn == "X":
        value = -12
        for move in moves:
            newgame = game
            newgame[move[0]][move[1]] = "X"
            newmove = minimax(newgame, "O")
            if newmove[0] > value:
                value = newmove[0] - 1
                bestmove = move
            newgame[move[0]][move[1]] = None
            
    else:
        value = 12
        for move in moves:
            newgame = game
            newgame[move[0]][move[1]] = "O"
            newmove = minimax(newgame, "X")
            if newmove[0] < value:
                value = newmove[0] + 1
                bestmove = move
            newgame[move[0]][move[1]] = None
    print (str(bestmove) + " gives " + str(value) + " on turn " + turn)  
    return (value, bestmove)