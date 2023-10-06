from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    with sqlite3.connect("data.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """)

init_db()

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        except sqlite3.IntegrityError:
            return jsonify({'status': 'error', 'message': 'Email already exists!'}), 400

    return jsonify({'status': 'success', 'message': 'Data saved successfully!'})

if __name__ == "__main__":
    app.run(debug=True)
