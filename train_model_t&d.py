import os
import markovify

DATASET_DIR = "dataset"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

def train(file):
    path = f"{DATASET_DIR}/{file}.txt"
    out = f"{MODEL_DIR}/{file}.json"

    print("Training", file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    model = markovify.NewlineText(text, retain_original=False)

    with open(out, "w", encoding="utf-8") as f:
        f.write(model.to_json())

    print("Saved →", out)


files = [
    "truth_easy", "truth_medium", "truth_hard",
    "truth_funny", "truth_romantic", "truth_dark",
    "truth_spicy", "truth_cringe", "truth_nsfw",

    "dare_easy", "dare_medium", "dare_hard",
    "dare_funny", "dare_romantic", "dare_dark",
    "dare_spicy", "dare_cringe", "dare_nsfw"
]

for file in files:
    train(file)

print("\nAll 18 ML models trained successfully! 🎉")
