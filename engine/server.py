from flask import Flask, jsonify, request, after_this_request
from pymongo import MongoClient
from flask_cors import CORS

client = MongoClient("mongodb://mongodb/")
db = client["musicologo"]
users = db["users"] 
songs = db["songs"] 
concerts = db["concerts"] 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def root():
    html = '''
    <html>
    <head>
    <title>Test</title>
    <body>
    <h1>PROVA</h1>
    </body>
    </html>
    '''
    return html

#crud per concerti, canzoni e utenti
@app.route("/add/user", methods=["POST"])
def add_user():
        jsondata = request.form
        user = {"username": jsondata["username"], "password": jsondata["password"]}
        res = users.insert_one(user)
        return jsonify({"created user": str(res.inserted_id)})

@app.route("/get/user/<username>", methods=["GET"])
def get_user(username):
    user = users.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route("/update/user/<username>", methods=["POST"])
def update_user(username):
    jsondata = request.form
    updated_user = {"$set": {"username": jsondata["username"], "password": jsondata["password"]}}
    res = users.update_one({"username": username}, updated_user)
    if res.modified_count > 0:
        return jsonify({"message": "User updated"})
    return jsonify({"message": "User not found or no changes made"}), 404

@app.route("/delete/user/<username>", methods=["POST"])
def delete_user(username):
    res = users.delete_one({"username": username})
    if res.deleted_count > 0:
        return jsonify({"message": "User deleted"})
    return jsonify({"message": "User not found"}), 404


@app.route("/add/song", methods=["POST"])
def add_song():
        jsondata = request.form
        song = {"title": jsondata["title"], "artist": jsondata["artist"], "discohouse": jsondata["discohouse"], "year": jsondata["year"], "posizione": jsondata["posizione"], "link": jsondata["link"]}
        res = songs.insert_one(song)
        return jsonify({"created song": str(res.inserted_id)})

@app.route("/get/song/<song_name>", methods=["GET"])
def get_song(song_name):
    song = songs.find_one({"title": song_name})
    if song:
        song["_id"] = str(song["_id"])
        return jsonify(song)
    return jsonify({"message": "Song not found"}), 404

@app.route("/get/songs", methods=["GET"])
def get_all_song():
    song = songs.find()
    if song:
        song = list(song)
        for singlesong in song:
            singlesong["_id"] = str(singlesong["_id"])
        return jsonify(song)
    return jsonify({"message": "Song not found"}), 404

@app.route("/update/song/<song_name>", methods=["POST"])
def update_song(song_name):
    jsondata = request.form
    updated_song = {"$set": {"name": jsondata["name"], "artist": jsondata["artist"]}}
    res = songs.update_one({"name": song_name}, updated_song)
    if res.modified_count > 0:
        return jsonify({"message": "Song updated"})
    return jsonify({"message": "Song not found or no changes made"}), 404

@app.route("/delete/song/<song_name>", methods=["POST"])
def delete_song(song_name):
    res = songs.delete_one({"name": song_name})
    if res.deleted_count > 0:
        return jsonify({"message": "Song deleted"})
    return jsonify({"message": "Song not found"}), 404


@app.route("/add/concert", methods=["POST"])
def add_artist():
        jsondata = request.form
        artist = {"data": jsondata["data"], "artista": jsondata["artista"], "luogo": jsondata["luogo"], "link": jsondata["link"], "foto": jsondata["foto"]}
        res = concerts.insert_one(artist)
        return jsonify({"created Concert": str(res.inserted_id)})

@app.route("/get/concert/<artist_name>", methods=["GET"])
def get_concerts(artist_name):
    concert = concerts.find_one({"artista": artist_name})
    if concert:
        concert["_id"] = str(concert["_id"])
        return jsonify(concert)
    return jsonify({"message": "Concert not found"}), 404

@app.route("/get/concerts", methods=["GET"])
def get_all_concerts():
    concert = concerts.find()
    if concert:
        concert = list(concert)
        for singleconcert in concert:
            singleconcert["_id"] = str(singleconcert["_id"])
        return jsonify(concert)
    return jsonify({"message": "Concert not found"}), 404

@app.route("/update/concert/<data>", methods=["POST"])
def update_concert(data):
    jsondata = request.form
    updated_concert = {"$set": {"artista": jsondata["artista"], "luogo": jsondata["luogo"], "artista": jsondata["data"]}}
    res = concerts.update_one({"data": data}, updated_concert)
    if res.modified_count > 0:
        return jsonify({"message": "Concert updated"})
    return jsonify({"message": "Concert not found or no changes made"}), 404

@app.route("/delete/concert/<data>", methods=["POST"])
def delete_concert(data):
    res = concerts.delete_one({"data": data})
    if res.deleted_count > 0:
        return jsonify({"message": "Concert deleted"})
    return jsonify({"message": "Concert not found"}), 404

@app.route("/login", methods=["POST"])
def login():
    jsondata = request.form
    user = users.find_one({"username": jsondata["username"], "password": jsondata["password"]})
    if user:
        return {"login": str(user["_id"])}, 200 #restituisco id utente, data la somiglianza a un hash sembra comodo
    return jsonify({"message": "user not found"}), 401 

