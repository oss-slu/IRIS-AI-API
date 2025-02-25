import os
import numpy as np
import faiss
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
from config import IMAGE_DIR, FAISS_INDEX_FILE, EMBEDDING_DIM
import boto3


BUCKET_NAME = 'iris-slu'
BUCKET_URL = f'https://{BUCKET_NAME}.s3.us-east-2.amazonaws.com/'

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Initialize FAISS index
index = faiss.IndexFlatL2(EMBEDDING_DIM)
image_urls = []


s3 = boto3.client('s3')

def get_image_embedding(image_path):
    """Extract CLIP embedding for an image."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    image_features /= image_features.norm(dim=-1, keepdim=True)  # Normalize
    return image_features.cpu().numpy()

# Process all images
for filename in os.listdir("images/"):
    if filename.endswith(".jpg",".png"):
        local_path = os.path.join("images/", filename)
        s3_path = "images/" + filename
        
        #check if the image is already in S3
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=s3_path)
        except:
            print(f"Uploading {filename} to S3...")
            s3.upload_file(local_path, BUCKET_NAME, s3_path)
            
        #store S3 URL instead of local path
        image_urls.append(BUCKET_URL + s3_path)
        
        # Get image embedding
        embedding = get_image_embedding(local_path)
        index.add(np.vstack([embedding]))
        

# Save FAISS index
faiss.write_index(index, FAISS_INDEX_FILE)
np.save("image_paths.npy", np.array(image_urls))
print(f"Indexed {len(image_urls)} images.")
