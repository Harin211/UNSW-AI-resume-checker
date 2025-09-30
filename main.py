from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import fitz  # PyMuPDF

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Save uploaded PDF temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # Save to outputs/
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/{os.path.splitext(file.filename)[0]}.txt"
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(text)

    # Clean temp file
    os.remove(file_path)

    # Return downloadable text file
    return FileResponse(output_path, media_type="text/plain", filename=os.path.basename(output_path))

