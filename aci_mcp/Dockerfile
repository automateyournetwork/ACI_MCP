FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source file
COPY main.py .
COPY urls.json .

# Ensure logs appear in real time
ENV PYTHONUNBUFFERED=1

# Run the server in stdio mode by default
ENTRYPOINT ["fastmcp", "run", "main.py"]
