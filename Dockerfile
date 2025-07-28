FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV XDG_CONFIG_HOME=/app/.config

# Install dependencies for Playwright + Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libgtk-3-0 libxss1 libasound2 libx11-xcb1 libdrm2 \
    libgbm1 libxcomposite1 libxdamage1 libxrandr2 \
    ca-certificates gnupg python3-distutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries
RUN playwright install chromium

# Copy all source code
COPY . .

#COPY input_chunks/ input_chunks/

# Run the script
CMD ["python", "main.py"]
