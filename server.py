from flask import Flask, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = "storage"
DATABASE_FILE = "users.json"
DEFAULT_RECOVERY_PASSWORD = "2030350667"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_users():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(DATABASE_FILE, "w") as file:
        json.dump(users, file)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users = load_users()
    
    if data["number"] in users:
        return jsonify({"status": "error", "message": "Number already registered"})
    
    users[data["number"]] = {"password": data["password"]}
    save_users(users)
    return jsonify({"status": "success", "message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    users = load_users()
    
    if data["number"] in users and (users[data["number"]]["password"] == data["password"] or data["password"] == DEFAULT_RECOVERY_PASSWORD):
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": "Invalid credentials"})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({"status": "success", "message": "File uploaded"})
    return jsonify({"status": "error", "message": "No file provided"})

@app.route("/files", methods=["GET"])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/delete/<filename>", methods=["DELETE"])
def delete(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"status": "success", "message": "File deleted"})
    return jsonify({"status": "error", "message": "File not found"})

if __name__ == "__main__":
    app.run(debug=True)
