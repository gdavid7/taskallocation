from ..parent_class import Model

from sentence_transformers import SentenceTransformer, util
import numpy as np

class Codebert(Model):
    def __init__(self, name):
        super().__init__(name)
        try:
            # Load a sentence transformer model (Choose a model suited for code + text)
            self.model = SentenceTransformer('microsoft/codebert-base-mlm')  # Using the MLM version which is more reliable
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    # Function to get embeddings
    def get_embedding(self, text):
        return self.model.encode(text, convert_to_numpy=True)
    
    # Function to compute cosine similarity
    def cosine_similarity(self, vec1, vec2):
        return util.cos_sim(vec1, vec2).item()

    # Function to compare two tasks
    def compare(self, task1, task2, weight_desc=0.6, weight_code=0.4):
        # Get description embeddings
        desc1_embed = self.get_embedding(task1["description"])
        desc2_embed = self.get_embedding(task2["description"])

        # Compute similarity for descriptions
        desc_similarity = self.cosine_similarity(desc1_embed, desc2_embed)

        # Check if both tasks have code
        if task1.get("code") and task2.get("code"):
            code1_embed = self.get_embedding(task1["code"])
            code2_embed = self.get_embedding(task2["code"])

            # Compute similarity for code snippets
            code_similarity = self.cosine_similarity(code1_embed, code2_embed)

            # Weighted combination of description & code similarity
            total_similarity = (weight_desc * desc_similarity) + (weight_code * code_similarity)
        else:
            # Use only description similarity if no code
            total_similarity = desc_similarity

        return total_similarity