FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Pillow/easy-pil if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run from root, easy python path resolution
CMD ["python", "src/bot.py"]
