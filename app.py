from flask import Flask, render_template, request, send_file
import pdfplumber
import os

app = Flask(__name__)
os.makedirs("outputs", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file or not file.filename.endswith(".pdf"):
        return "Please upload a valid PDF."

    # Save temporarily
    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    # Extract text
    all_text = ""
    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"

    # Save text file
    output_path = os.path.join("outputs", f"{os.path.splitext(file.filename)[0]}.txt")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(all_text)

    # Clean up temp file
    os.remove(temp_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
