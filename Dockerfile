FROM python:3.12-slim

WORKDIR /app

# OpenCV için gerekli sistem kütüphaneleri
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# requirements kurulumu
RUN pip install --no-cache-dir -r requirements.txt

# Model ve kodları kopyala
COPY . .

# Port ayarı (Bulut sağlayıcıların çevre değişkeni desteği için)
ENV PORT=5000

# Sunucuyu başlat
CMD ["python", "server.py"]
