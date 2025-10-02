from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

class TextData(BaseModel):
    text: str

df = pd.read_csv("courses_7.csv")
df["FullText"] = (
    df["course_id"].astype(str) + " - " +
    df["course_name"].astype(str) + " - " +
    df["faculty"].astype(str) + " - " +
    df["school"].astype(str) + " - " +
    df["overview"].astype(str)
)

courses = dict(zip(df["course_code"], df["FullText"]))
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.post("/analyze_text/")
async def analyze_text(data: TextData):
    resume_text = data.text

    # Embed resume and courses
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    course_embs = model.encode(list(courses.values()), convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.cos_sim(resume_emb, course_embs)[0]

    # Get top 15 courses
    top_idx = scores.argsort(descending=True)[:15]
    results = []
    for i in top_idx:
        name = list(courses.keys())[i]
        score = scores[i].item()
        results.append(f"{name}")

    output_str = "\n".join(results)
    return {"result": output_str}
