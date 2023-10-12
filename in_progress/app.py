from flask import Flask, redirect, url_for, request, render_template, send_file
from pymongo.mongo_client import MongoClient
import os
from pymongo.server_api import ServerApi
from config import URI_

app = Flask(__name__)

uri = URI_

# Connect to MongoDB
client = MongoClient(uri)
db = client['mp3Ceo']  
file_collection = db['mp3_files']

audio_files = [
    'DrAmenBrain.wav',
    'foods.wav',
    'Habits.wav'
]

@app.route('/')
def index():
    return render_template('index.html', audio_files=audio_files)

@app.route('/audio/<filename>')
def get_audio(filename):
    audio_path = os.path.join('mp3_files', filename)
    return send_file(audio_path, mimetype='audio/mpeg')

@app.route('/get_wav')
def get_audio():
    audio_files = file_collection.find({}, {'_id': 0, 'name': 1, 'path': 1})

    return render_template('index.html', audio_files=audio_files)


@app.route('/')
def todo():
    _items = file_collection.find()
    items = [item for item in _items]
    return render_template('todo.html', items=items)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
