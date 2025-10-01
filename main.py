# main.py
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

# Temporary storage for last result
results_store = {}

# Friend server URL
FRIEND_SERVER_URL = "http://192.168.50.232:8000/analyze_text/"  # change if needed

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Save PDF temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    doc = fitz.open(file_path)
    resume_text = "".join(page.get_text() or "" for page in doc)
    doc.close()
    os.remove(file_path)

    # Convert to JSON
    payload = {"text": resume_text}
    print("📄 Sending to friend server:")
    print(json.dumps(payload, indent=2))

    # Send to friend's server
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(FRIEND_SERVER_URL, json=payload)
            friend_result = response.json()
    except Exception as e:
        friend_result = {"result": f"Could not reach friend server: {e}"}

    print("📄 Friend server returned:")
    print(json.dumps(friend_result, indent=2))

    # Store result for results page
    results_store["last"] = friend_result

    # Render results page immediately
    courses_list = friend_result.get("result", "").split("\n")
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "courses": courses_list}

