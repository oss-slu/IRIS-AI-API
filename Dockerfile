# Use NVIDIA's official CUDA base image with Python 3.8
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Copy the application files
COPY . .

# Use Gunicorn for better performance
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
