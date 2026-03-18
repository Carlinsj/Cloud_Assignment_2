from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["tododb"]
todos = db["todos"]

@app.route('/')
def index():
    all_todos = list(todos.find())
    return render_template('index.html', todos=all_todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todos.insert_one({"task": task})
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    from bson.objectid import ObjectId
    todos.delete_one({"_id": ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)