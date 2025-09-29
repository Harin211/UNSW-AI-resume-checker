from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

@app.post("/convert_resume/")
async def convert_resume(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Convert PDF to text
    import fitz  # PyMuPDF
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # (Optional) Save in outputs folder on Railway
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/{os.path.splitext(file.filename)[0]}.txt"
    with open(output_path, "w") as out:
        out.write(text)

    # Return the text directly
    return {"filename": file.filename, "text": text[:1000]}  # limit preview
