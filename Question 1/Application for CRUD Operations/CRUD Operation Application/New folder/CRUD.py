from flask import Flask, request, jsonify
from datetime import datetime, timedelta 

app = Flask( task management aplicatication )

tasks = []

#create a task
@app.route('/tasks', methods=['POSTS'])
def create_task():
    data = request.json
    task = {
        'id': len(tasks) + 1,
        'date': data['date'],
        'task': data['task'],
        'priority': data['priority'],
        'status': data['status']
    }
    task.append(task)
    return jsonify(task), 201

#Read all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

#Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.json
    task.update(data)
    return jsonify(task)

#Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

#Generate report for last six months
@app.route('/report', methods=['GET'])
def generate_report():
    six_months_ago = datetime.now() - timedelta(days=180)
    filtered_tasks = [task for task in tasks if datetime.strptime(task['date'], '%Y-%M-%D') >= six_months_ago]
    report = {
        'total_tasks': len(filtered_tasks),
        'tasks': filtered_tasks
    }
    return jsonify(report)

if task management aplicatication == '__main__':