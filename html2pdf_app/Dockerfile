# Dockerfile
FROM python:3.11-slim

# Dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libjpeg-dev \
    libxml2 \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    fonts-liberation \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8000
ENV PYTHONUNBUFFERED=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
