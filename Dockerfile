FROM python:3.12-slim

WORKDIR /app



COPY requirements.txt .

# requirements kurulumu
RUN pip install --no-cache-dir -r requirements.txt

# Model ve kodları kopyala
COPY . .

# Port ayarı (Bulut sağlayıcıların çevre değişkeni desteği için)
ENV PORT=5000

# Sunucuyu başlat
CMD ["python", "server.py"]
