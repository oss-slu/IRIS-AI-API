import os
import numpy as np
import faiss
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
from config import IMAGE_DIR, FAISS_INDEX_FILE, EMBEDDING_DIM

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Initialize FAISS index
index = faiss.IndexFlatL2(EMBEDDING_DIM)
image_paths = []

def get_image_embedding(image_path):
    """Extract CLIP embedding for an image."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    image_features /= image_features.norm(dim=-1, keepdim=True)  # Normalize
    return image_features.cpu().numpy()

# Process all images
for filename in os.listdir(IMAGE_DIR):
    if filename.endswith((".jpg", ".png")):
        path = os.path.join(IMAGE_DIR, filename)
        image_paths.append(path)
        embedding = get_image_embedding(path)
        index.add(np.vstack([embedding]))  # Add to FAISS index

# Save FAISS index
faiss.write_index(index, FAISS_INDEX_FILE)
np.save("image_paths.npy", np.array(image_paths))
print(f"Indexed {len(image_paths)} images.")
