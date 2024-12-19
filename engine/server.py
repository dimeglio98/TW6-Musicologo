from flask import Flask, jsonify, request, after_this_request
from pymongo import MongoClient

client = MongoClient("mongodb://mongodb/")
db = client["musicologo"]
users = db["users"] 
songs = db["songs"] 
albums = db["albums"] 
artists = db["artists"] 

app = Flask(__name__)

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

#crud per artisti, canzoni, album e utenti
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
        song = {"name": jsondata["name"], "artist": jsondata["artist"], "album": jsondata["album"], "airings": jsondata["airings"], "posizione": jsondata["posizione"], "link": jsondata["link"]}
        res = songs.insert_one(song)
        return jsonify({"created song": str(res.inserted_id)})

@app.route("/get/song/<song_name>", methods=["GET"])  # Changed to search by name
def get_song(song_name):
    song = songs.find_one({"name": song_name})
    if song:
        song["_id"] = str(song["_id"])
        return jsonify(song)
    return jsonify({"message": "Song not found"}), 404

@app.route("/update/song/<song_name>", methods=["POST"]) # Changed to update by name
def update_song(song_name):
    jsondata = request.form
    updated_song = {"$set": {"name": jsondata["name"], "artist": jsondata["artist"]}}
    res = songs.update_one({"name": song_name}, updated_song)
    if res.modified_count > 0:
        return jsonify({"message": "Song updated"})
    return jsonify({"message": "Song not found or no changes made"}), 404

@app.route("/delete/song/<song_name>", methods=["POST"]) # Changed to delete by name
def delete_song(song_name):
    res = songs.delete_one({"name": song_name})
    if res.deleted_count > 0:
        return jsonify({"message": "Song deleted"})
    return jsonify({"message": "Song not found"}), 404


@app.route("/add/album", methods=["POST"])
def add_album():
        jsondata = request.form
        album = {"name": jsondata["name"], "artist": jsondata["artist"]}
        res = albums.insert_one(album)
        return jsonify({"created album": str(res.inserted_id)})

@app.route("/get/album/<album_name>", methods=["GET"])
def get_album(album_name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    album = songs.find({"album": album_name}, {'_id': 0}) #con la seconda {} sto disabilitando la visione dell'id perche problematica nel return
    if album:
        return jsonify(list(album))
    return jsonify({"message": "Album not found"}), 404

@app.route("/update/album/<album_name>", methods=["POST"])
def update_album(album_name):
    jsondata = request.form
    updated_album = {"$set": {"name": jsondata["name"], "artist": jsondata["artist"]}}
    res = albums.update_one({"name": album_name}, updated_album)
    if res.modified_count > 0:
        return jsonify({"message": "Album updated"})
    return jsonify({"message": "Album not found or no changes made"}), 404

@app.route("/delete/album/<album_name>", methods=["POST"])
def delete_album(album_name):
    res = albums.delete_one({"name": album_name})
    if res.deleted_count > 0:
        return jsonify({"message": "Album deleted"})
    return jsonify({"message": "Album not found"}), 404


@app.route("/add/artist", methods=["POST"])
def add_artist():
        jsondata = request.form
        artist = {"name": jsondata["name"], "surname": jsondata["surname"]}
        res = artists.insert_one(artist)
        return jsonify({"created artist": str(res.inserted_id)})

@app.route("/get/artist/<artist_name>", methods=["GET"])
def get_artist(artist_name):
    artist = artists.find_one({"name": artist_name})
    if artist:
        artist["_id"] = str(artist["_id"])
        return jsonify(artist)
    return jsonify({"message": "Artist not found"}), 404

@app.route("/update/artist/<artist_name>", methods=["POST"])
def update_artist(artist_name):
    jsondata = request.form
    updated_artist = {"$set": {"name": jsondata["name"], "surname": jsondata["surname"]}}
    res = artists.update_one({"name": artist_name}, updated_artist)
    if res.modified_count > 0:
        return jsonify({"message": "Artist updated"})
    return jsonify({"message": "Artist not found or no changes made"}), 404

@app.route("/delete/artist/<artist_name>", methods=["POST"])
def delete_artist(artist_name):
    res = artists.delete_one({"name": artist_name})
    if res.deleted_count > 0:
        return jsonify({"message": "Artist deleted"})
    return jsonify({"message": "Artist not found"}), 404

@app.route("/login", methods=["POST"])
def login():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    jsondata = request.form
    user = users.find_one({"username": jsondata["username"], "password": jsondata["password"]})
    if user:
        return {"login": str(user["_id"])}, 200 #restituisco id utente, data la somiglianza a un hash sembra comodo
    return jsonify({"message": "user not found"}), 401 

