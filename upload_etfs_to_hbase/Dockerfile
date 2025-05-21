FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required to build thriftpy2
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY upload_etfs_to_hbase.py ./
COPY ETFs ./ETFs

CMD ["python", "upload_etfs_to_hbase.py"]
