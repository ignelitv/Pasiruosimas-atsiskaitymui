from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask import session

app = Flask(__name__)

# Sukurkime SQLite duomenų bazę ir prisijunkime prie jos
conn = sqlite3.connect('notes.db')
c = conn.cursor()

# Sukurkime lentelę vartotojams
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             username TEXT NOT NULL,
             password TEXT NOT NULL)''')

# Sukurkime lentelę užrašams
c.execute('''CREATE TABLE IF NOT EXISTS notes (
             id INTEGER PRIMARY KEY,
             user_id INTEGER NOT NULL,
             note TEXT NOT NULL,
             FOREIGN KEY (user_id) REFERENCES users (id))''')

# Įrašykime pavyzdinius duomenis į lentelę
c.execute("INSERT INTO users (username, password) VALUES ('user1', 'password1')")
c.execute("INSERT INTO users (username, password) VALUES ('user2', 'password2')")

# Išsaugokime pakeitimus ir uždarykime prisijungimą prie duomenų bazės
conn.commit()
conn.close()

# Toliau eitų jūsų maršrutai ir kita programos logika

# Sukurkime prisijungimui/registracijai skirtus maršrutus
@app.route('/')
def index():
    return render_template('index.html')

# Tikriname vartotojo prisijungimo duomenis
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return redirect(url_for('user_notes'))
    else:
        return "Invalid username or password"

# Įrašome naują vartotoją į duomenų bazę
@app.route('/register', methods=['POST'])
def register():
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Vartotojo užrašų puslapis
@app.route('/notes/<username>')
def user_notes(username):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = c.fetchone()[0]
    c.execute("SELECT note FROM notes WHERE user_id=?", (user_id,))
    notes = c.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)

# Įrašome naują vartotojo užrašą į duomenų bazę
@app.route('/add_note', methods=['POST'])
def add_note():
    new_note = request.form['new_note']
    username = session['username']  # Gauti vartotojo vardą iš sesijos
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = c.fetchone()[0]
    c.execute("INSERT INTO notes (user_id, note) VALUES (?, ?)", (user_id, new_note))
    conn.commit()
    conn.close()
    return redirect(url_for('user_notes', username=username))

# Visų vartotojų sąrašo puslapis
@app.route('/all_users')
def all_users():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('all_users.html', users=users)

# Pasirinkto vartotojo užrašų puslapis
@app.route('/user_notes/<username>')
def user_notes_admin(username):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = c.fetchone()[0]
    c.execute("SELECT note FROM notes WHERE user_id=?", (user_id,))
    notes = c.fetchall()
    conn.close()
    return render_template('user_notes_admin.html', username=username, notes=notes)

if __name__ == '__main__':
    app.run(debug=True)
