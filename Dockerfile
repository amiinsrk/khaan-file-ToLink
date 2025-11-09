FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Rakib dependencies muhiim ah oo Koyeb aqbasho
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        git \
        build-essential \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies oo rakib
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy code-ka intiisa kale
COPY . .

# Si thunder.sh uu u noqdo executable
RUN chmod +x thunder.sh

# Start the bot
CMD ["bash", "thunder.sh"]

