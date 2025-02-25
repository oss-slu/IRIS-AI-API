from flask import Flask, request, jsonify
import os
from search import find_similar_images

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/search", methods=["POST"])
def search_images():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["image"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    similar_images = find_similar_images(file_path, k=5)

    return jsonify({"similar_images": similar_images})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
