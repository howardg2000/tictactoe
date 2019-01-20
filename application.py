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
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]] * 9
        session["turn"] = "X"
        session["move"] = 0
        session["playing"] = True
    
    return render_template("game.html", game=session["board"][session["move"]], turn=session["turn"], playing=session["playing"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    
    session["move"] += 1
    session["board"][1][row][col] = session["turn"]

    game = session["board"][session["move"]]

    if game[row][0] == game[row][1] == game[row][2] or game[0][col] == game[1][col] == game[2][col] or checkDiagonals():
        session["playing"] = False
    elif session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

def checkDiagonals():
    game = session["board"][session["move"]]
    if game[1][1]:
        return game[0][0]==game[1][1]==game[2][2] or game[2][0]==game[1][1]==game[0][2]
    return False