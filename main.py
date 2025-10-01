from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import fitz
import json
import httpx  # async HTTP requests

app = FastAPI()

# Mount static folder for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Replace with your friend's server URL
# Correct endpoint URL
FRIEND_SERVER_URL = "http://192.168.50.232:8000/analyze_text/"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    # 1️⃣ Save uploaded PDF temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2️⃣ Extract text from PDF
    doc = fitz.open(file_path)
    resume_text = "".join(page.get_text() or "" for page in doc)
    doc.close()
    os.remove(file_path)

    # 3️⃣ Convert to JSON
    payload = {"text": resume_text}
    print(payload)

    # 4️⃣ Send JSON to friend's server
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(FRIEND_SERVER_URL, json=payload)
            friend_result = response.json()
    except Exception as e:
        friend_result = {"error": f"Could not reach friend server: {e}"}

    # 5️⃣ Print friend server's JSON in your terminal
    print("📄 Friend server returned:")
    print(json.dumps(friend_result, indent=2))

    # 6️⃣ Render index.html and pass a success message
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": "✅ PDF processed and sent to friend server!"}
    )
