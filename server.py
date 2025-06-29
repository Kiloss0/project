from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    tasks = load_tasks()
    tasks.append({"text": data['text'], "completed": False})
    save_tasks(tasks)
    return jsonify({"status": "ok"})

@app.route('/tasks/<int:index>', methods=['PUT'])
def update_task(index):
    data = request.json
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['completed'] = data['completed']
        save_tasks(tasks)
        return jsonify({"status": "updated"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/tasks/<int:index>', methods=['DELETE'])
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == '__main__':
    app.run(debug=True)
