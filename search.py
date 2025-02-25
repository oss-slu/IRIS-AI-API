import faiss
import numpy as np
from indexer import get_image_embedding

# Load FAISS index and image URLs
FAISS_INDEX_FILE = "faiss_index.bin"
IMAGE_URLS_FILE = "image_urls.npy"

# Load the FAISS index
index = faiss.read_index(FAISS_INDEX_FILE)

# Load stored S3 URLs instead of local file paths
image_urls = np.load(IMAGE_URLS_FILE)

def find_similar_images(query_image_path, k=5):
    """
    Find the top-k similar images and return their S3 URLs.
    
    Parameters:
        query_image_path (str): Path to the query image.
        k (int): Number of similar images to return.

    Returns:
        List[str]: List of S3 image URLs.
    """
    # Get the embedding of the query image
    query_embedding = get_image_embedding(query_image_path)
    
    # Search FAISS for similar embeddings
    distances, indices = index.search(query_embedding, k)

    # Retrieve the corresponding image URLs
    return [image_urls[i] for i in indices[0]]

# Test the function
if __name__ == "__main__":
    test_image = "path/to/test-image.jpg"  # Replace with an actual test image
    results = find_similar_images(test_image, k=5)
    print("Similar Images:", results)
