from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from search import find_similar_images

app = Flask(__name__)
CORS(app)  # ✅ Allows all origins

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/search", methods=["POST"])
def search_images():
    data = request.json
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400
    
    try:
        # Extract Base64 image string
        base64_image = data["image"].split(",")[1]  # Remove 'data:image/jpeg;base64,' prefix if present
        
        # Decode Base64 to binary image data
        image_data = base64.b64decode(base64_image)

        # Define file path to save the image
        file_path = os.path.join(UPLOAD_FOLDER, "uploaded_image.jpg")
        
        # Save the image file
        with open(file_path, "wb") as f:
            f.write(image_data)

        # Process the image with your function
        similar_images = find_similar_images(file_path, k=5)

        return jsonify({"similar_images": similar_images})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
