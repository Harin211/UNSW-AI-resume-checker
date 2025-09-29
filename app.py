from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import os

app = FastAPI()

# Allow frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure outputs folder exists
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)


@app.post("/convert_resume/")
async def convert_resume(file: UploadFile = File(...)):
    try:
        # Save uploaded PDF temporarily
        pdf_path = os.path.join(output_dir, file.filename)
        with open(pdf_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"

        # Save extracted text
        txt_filename = os.path.splitext(file.filename)[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(all_text)

        return {"text": all_text, "text_file": txt_filename}

    except Exception as e:
        return {"error": str(e)}
