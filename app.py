from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Config
UPLOAD_FOLDER = "uploads"
FASTAPI_URL = "https://web-production-62be6.up.railway.app/convert_resume/"  # your FastAPI endpoint
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Forward file to FastAPI backend
        with open(filepath, "rb") as f:
            response = requests.post(
                FASTAPI_URL,
                files={"file": (file.filename, f, "application/pdf")}
            )

        if response.status_code != 200:
            return jsonify({"error": "Failed to process PDF", "details": response.text}), 500

        data = response.json()
        return jsonify({"status": "success", "filename": file.filename, "text": data.get("text", "")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
