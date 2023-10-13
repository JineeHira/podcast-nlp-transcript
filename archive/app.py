from flask import Flask, redirect, url_for, request, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['mp3Ceo']
file_collection = db['mp3_files']

mp3_files = [
    {'name': 'file1.mp3', 'path': '/app/mp3_files/file1.mp3'},
    {'name': 'file2.mp3', 'path': '/app/mp3_files/file2.mp3'},
    
]

# Insert the data into the MongoDB collection
file_collection.insert_many(mp3_files)

@app.route('/')
def todo():

    _items = db.ceo_apidb.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }

    db.ceo_apidb.insert_one(item_doc)
    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
