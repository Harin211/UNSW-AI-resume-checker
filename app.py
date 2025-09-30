from flask import Flask, render_template, request, jsonify # type: ignore
import os

app = Flask(__name__)

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

    # Save temporarily
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # TODO: Call your FastAPI backend here (requests.post)
    # For now just dummy response
    return jsonify({"status": "success", "filename": file.filename})

if __name__ == '__main__':
    app.run(debug=True)
