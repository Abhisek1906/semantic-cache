from sentence_transformers import SentenceTransformer

# Load once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    return model.encode(text, batch_size=1, show_progress_bar=False).tolist()

def normalize(text: str):
    return text.lower().strip()