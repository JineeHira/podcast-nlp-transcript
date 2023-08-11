from flask import Flask, redirect, url_for, request, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://jineehira1:MnXWAHg8RgqVGd3n@ceomp3.z8bilj6.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient("mongodb", 27017)
db = client.ceo_apidb

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
