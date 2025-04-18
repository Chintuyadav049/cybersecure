# app.py
from flask import Flask, render_template, request, redirect
from faker import Faker
import sqlite3
from datetime import datetime

app = Flask(__name__)
fake = Faker()

REAL_USERS = {
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3",
    "user4": "pass4",
    "user5": "pass5",
    "user6": "pass6",
    "user7": "pass7",
    "user8": "pass8",
    "user9": "pass9",
    "user10": "pass10"
}

# Create DB and table if not exists
def init_db():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    ip TEXT,
                    is_fake INTEGER,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

def get_real_data():
    return {
        'name': 'Alice Johnson',
        'email': 'alice.johnson@securemail.com',
        'ssn': '123-45-6789',
        'balance': '$9,240.00'
    }

def get_fake_data():
    return {
        'name': fake.name(),
        'email': fake.email(),
        'ssn': fake.ssn(),
        'balance': f"${fake.random_int(min=1000, max=10000)}"
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    username = None
    data = None
    logs = None
    is_fake = True

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

        if username in REAL_USERS and REAL_USERS[username] == password:
            is_fake = False

        conn = sqlite3.connect("logs.db")
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO logs (username, ip, is_fake, timestamp) VALUES (?, ?, ?, ?)",
                  (username, ip, int(is_fake), timestamp))
        conn.commit()

        if not is_fake:
            c.execute("SELECT username, ip, is_fake, timestamp FROM logs")
            logs = c.fetchall()

        conn.close()

        data = get_real_data() if not is_fake else get_fake_data()

    return render_template('index.html', username=username, data=data, logs=logs, is_fake=is_fake)

if __name__ == '__main__':
    app.run(debug=True)
