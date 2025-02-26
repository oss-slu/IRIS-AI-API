# Use NVIDIA's CUDA base image with Python 3.8
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*  # Clean up

# Copy the application files
COPY . .

# Set up a virtual environment inside /app/venv
RUN python3 -m venv /app/venv

# Activate venv and install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Use Gunicorn with the venv
CMD ["/app/venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
