# main.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import fitz
import os
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Friend's server URL
FRIEND_SERVER_URL = "http://192.168.50.232:8000/analyze_text/"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    # 1️⃣ Convert PDF → text
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    doc = fitz.open(file_path)
    resume_text = "".join(page.get_text() or "" for page in doc)
    doc.close()
    os.remove(file_path)

    # 2️⃣ Optional: save locally
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/{os.path.splitext(file.filename)[0]}.txt"
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(resume_text)

    # 3️⃣ Send resume text to friend's AI server
    payload = {"text": resume_text}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(FRIEND_SERVER_URL, json=payload)
        result = response.json().get("result", "No result returned")
    except Exception as e:
        result = f"Could not contact friend server: {str(e)}"

    # 4️⃣ Return result to template
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )
