import os

# Directory for stored images
IMAGE_DIR = "images/"

# FAISS index file
FAISS_INDEX_FILE = "faiss_index.bin"

# AWS S3 Configuration (if using S3 for storage)
AWS_BUCKET_NAME = "your-s3-bucket-name"
AWS_REGION = "us-east-1"

# Model parameters
EMBEDDING_DIM = 512  # CLIP ViT-B/32 outputs 512-d embeddings
