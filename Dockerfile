FROM python:3.12-slim

WORKDIR /app



COPY requirements.txt .

# Ultralytics otomatik olarak opencv-python kuruyor ve hata verdiriyor. 
# Bu yüzden onu silip sadece headless (sunucu) sürümünü bırakıyoruz.
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y opencv-python \
    && pip install --no-cache-dir opencv-python-headless

# Model ve kodları kopyala
COPY . .

# Port ayarı (Bulut sağlayıcıların çevre değişkeni desteği için)
ENV PORT=5000

# Sunucuyu başlat
CMD ["python", "server.py"]
