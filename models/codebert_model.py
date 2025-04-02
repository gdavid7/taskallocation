from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load a sentence transformer model (Choose a model suited for code + text)
model = SentenceTransformer("microsoft/codebert-base")  # Can replace with "codebert-base" for code-specific tasks

# Function to get embeddings
def get_embedding(text):
    return model.encode(text, convert_to_numpy=True)

# Function to compute cosine similarity
def cosine_similarity(vec1, vec2):
    return util.cos_sim(vec1, vec2).item()

# Function to compare two tasks
def compare_tasks_cb(task1, task2, weight_desc=0.6, weight_code=0.4):
    # Get description embeddings
    desc1_embed = get_embedding(task1["description"])
    desc2_embed = get_embedding(task2["description"])

    # Compute similarity for descriptions
    desc_similarity = cosine_similarity(desc1_embed, desc2_embed)

    # Check if both tasks have code
    if task1.get("code") and task2.get("code"):
        code1_embed = get_embedding(task1["code"])
        code2_embed = get_embedding(task2["code"])

        # Compute similarity for code snippets
        code_similarity = cosine_similarity(code1_embed, code2_embed)

        # Weighted combination of description & code similarity
        total_similarity = (weight_desc * desc_similarity) + (weight_code * code_similarity)
    else:
        # Use only description similarity if no code
        total_similarity = desc_similarity

    return total_similarity