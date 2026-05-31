# Gunakan base image Python 3.9 slim yang sangat ringan
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements terlebih dahulu untuk memanfaatkan caching layer Docker
COPY requirements.txt .

# Install semua library yang diperlukan (tanpa cache agar ukuran image lebih kecil)
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi (mengikuti batasan .dockerignore) ke dalam container
COPY . .

# Berikan port standar untuk aplikasi di Hugging Face Spaces
EXPOSE 7860

# Jalankan Flask App menggunakan Gunicorn untuk production yang stabil
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "2", "--threads", "4", "--timeout", "120"]
