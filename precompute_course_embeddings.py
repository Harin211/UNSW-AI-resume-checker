import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

CSV_PATH = "courses_7.csv"
MODEL_NAME = "all-mpnet-base-v2"
OUTPUT_PATH = "course_embeddings.pt"

print("Loading model...")
model = SentenceTransformer(MODEL_NAME, device="cuda" if torch.cuda.is_available() else "cpu")

print("Reading courses CSV...")
df = pd.read_csv(CSV_PATH)

print(f"Encoding {len(courses_text)} courses...")
df["FullText"] = (
    df["course_id"].astype(str) + " - " +
    df["course_name"].astype(str) + " - " +
    df["faculty"].astype(str) + " - " +
    df["school"].astype(str) + " - " +
    df["overview"].astype(str)
)

courses = dict(zip(df["course_code"], df["FullText"]))
course_embs = model.encode(list(courses.values()), convert_to_tensor=True)

torch.save({
    "embeddings": course_embs,
    "courses": df.to_dict(orient="records")
}, OUTPUT_PATH)

print(f"Saved embeddings to {OUTPUT_PATH}")
