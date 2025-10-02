from fastapi import FastAPI
from pydantic import BaseModel
import torch
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

class TextData(BaseModel):
    text: str

# === Load precomputed data and model once at startup ===
DATA_PATH = "course_embeddings_2.pt"
MODEL_NAME = "all-mpnet-base-v2"

print("Loading model...")
model = SentenceTransformer(MODEL_NAME, device="cuda" if torch.cuda.is_available() else "cpu")

print("Loading precomputed course embeddings...")
data = torch.load(DATA_PATH, map_location="cuda" if torch.cuda.is_available() else "cpu")
course_embs = data["embeddings"]
courses = data["courses"]

print(f"Loaded {len(courses)} courses.")

@app.post("/analyze_text/")
async def analyze_text(data: TextData):
    resume_text = data.text

    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    scores = util.cos_sim(resume_emb, course_embs)[0]

    top_idx = torch.topk(scores, k=15).indices
    results = []

    for i in top_idx:
        course = courses[i]
        course_name = f"{course['course_code']} - {course['course_name']}"
        results.append(course_name)

    output_str = "\n".join(results)
    return {"result": output_str}
