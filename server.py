from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import json

app = Flask(__name__, static_folder='../webapp' if __name__ == '__main__' else 'webapp')

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, mafia_boost INTEGER DEFAULT 0, extra_actions INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT mafia_boost, extra_actions FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"mafia_boost": row[0], "extra_actions": row[1]})
    return jsonify({"mafia_boost": 0, "extra_actions": 0})

@app.route('/api/add_boost', methods=['POST'])
def add_boost():
    data = request.json
    user_id = data['user_id']
    boost_type = data['type']
    amount = data['amount']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, mafia_boost, extra_actions) VALUES (?, 0, 0)", (user_id,))
    if boost_type == "mafia":
        c.execute("UPDATE users SET mafia_boost = mafia_boost + ? WHERE user_id = ?", (amount, user_id))
    elif boost_type == "actions":
        c.execute("UPDATE users SET extra_actions = extra_actions + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json
    return jsonify({
        "invoice_payload": json.dumps(data),
        "title": data['title'],
        "description": data['description'],
        "payload": json.dumps(data),
        "currency": "XTR",
        "prices": [{"label": data['title'], "amount": data['price']}]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)