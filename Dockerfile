# Use NVIDIA's CUDA base image with Python 3.8
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*  # Clean up

# Set up a virtual environment inside /app/venv
RUN python3 -m venv /app/venv

# Copy only the requirements file first (optimizing caching)
COPY requirements.txt .

# Activate venv and install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application files
COPY . .

# Expose Flask port
EXPOSE 5000

# Use Gunicorn with the venv
CMD ["/app/venv/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
