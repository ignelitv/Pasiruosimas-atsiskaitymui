from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def sukurkti_lentele():
    conn = sqlite3.connect('duomenys.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS uzrasai
                 (id INTEGER PRIMARY KEY, vartotojas TEXT, tekstas TEXT)''')
    conn.commit()
    conn.close()

def saugoti_db(vartotojas, tekstas):
    conn = sqlite3.connect('duomenys.db')
    c = conn.cursor()
    c.execute("INSERT INTO uzrasai (vartotojas, tekstas) VALUES (?, ?)", (vartotojas, tekstas))
    conn.commit()
    conn.close()

def skaityti_db(vartotojas):
    conn = sqlite3.connect('duomenys.db')
    c = conn.cursor()
    c.execute("SELECT * FROM uzrasai WHERE vartotojas = ? ORDER BY id DESC", (vartotojas,))
    data = c.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registruoti_vartotoja', methods=['POST'])
def registruoti_vartotoja():
    vardas = request.form['vartotojas']
    sukurkti_lentele()  # Užtikriname, kad lentele būtų sukurta
    return redirect(url_for('vartotojas', vardas=vardas))

@app.route('/vartotojai/<vardas>', methods=['GET', 'POST'])
def vartotojas(vardas):
    if request.method == 'POST':
        tekstas = request.form['tekstas']
        saugoti_db(vardas, tekstas)
    uzrasai = skaityti_db(vardas)
    return render_template('vartotojas.html', vardas=vardas, uzrasai=uzrasai)

if __name__ == '__main__':
    app.run(debug=True)
