## Parent image
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Make sure /app is on PYTHONPATH
ENV PYTHONPATH=/app

EXPOSE 8501
EXPOSE 9999

# 👇 Run as a package
CMD ["python", "-m", "app.main"]
