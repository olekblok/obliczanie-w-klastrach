FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc && \
    pip install --upgrade pip && \
    pip install flask happybase thriftpy2

COPY app.py .
COPY load_data.py /app/load_data.py


CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
