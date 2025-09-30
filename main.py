from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import fitz  # PyMuPDF
from analyze import count_letters  # <-- import analysis function

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/upload/", response_class=HTMLResponse)
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
    os.remove(file_path)

    # Run analysis
    letter_count = count_letters(text)

    # Render result in UI
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": f"The PDF contains {letter_count} letters."}
    )
