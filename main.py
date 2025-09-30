from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import fitz  # PyMuPDF
import httpx  # for sending requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Replace with your friend's server URL
FRIEND_SERVER_URL = "http://192.168.50.232:8000/analyze_text/"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    # 1️⃣ Save uploaded PDF temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2️⃣ Extract text
    doc = fitz.open(file_path)
    resume_text = "".join(page.get_text() or "" for page in doc)
    doc.close()
    os.remove(file_path)

    # 3️⃣ Send text to friend's AI server
    payload = {"text": resume_text}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(FRIEND_SERVER_URL, json=payload)
        ai_result = response.json().get("result", "No result returned")
    except Exception as e:
        ai_result = f"Could not contact friend server: {str(e)}"

    # 4️⃣ Render result in the same UI
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": ai_result}
    )
