from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()

# Sukuriamas lenteles, jei ji neegzistuoja
create_table()

# Pagrindinis puslapis
@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

# Vartotojo užrašų puslapis
@app.route('/notes', methods=['GET', 'POST'])
def user_notes():
    if request.method == 'POST':
        note_content = request.form['note']
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (content) VALUES (?)", (note_content,))
        conn.commit()
        conn.close()
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)

if __name__ == '__main__':
    app.run(debug=True)
