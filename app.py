from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados para la API
tasks = [
    {"id": 1, "title": "Aprender Flask", "done": False},
    {"id": 2, "title": "Escribir una API REST", "done": True},
]

# Ruta principal
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenido a la API de Tareas"})


# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


# Obtener una tarea específica por ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task)


# Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    new_task["id"] = tasks[-1]["id"] + 1 if tasks else 1
    tasks.append(new_task)
    return jsonify(new_task), 201


# Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404

    updates = request.json
    task.update(updates)
    return jsonify(task)


# Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task_exists = any(task for task in tasks if task["id"] == task_id)
    
    if not task_exists:
        return jsonify({"error": "Tarea no encontrada"}), 404

    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Tarea eliminada"}), 200


if __name__ == '__main__':
    app.run(debug=True)
