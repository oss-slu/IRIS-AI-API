import faiss
import numpy as np
from config import FAISS_INDEX_FILE, IMAGE_DIR, EMBEDDING_DIM
from indexer import get_image_embedding

# Load FAISS index
index = faiss.read_index(FAISS_INDEX_FILE)
image_paths = np.load("image_paths.npy")

def find_similar_images(query_image_path, k=5):
    """Find the top-k similar images to a given query image."""
    query_embedding = get_image_embedding(query_image_path)
    distances, indices = index.search(query_embedding, k)
    
    return [image_paths[i] for i in indices[0]]
