import os
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load Model Machine Learning
MODEL_PATH = "model.joblib"
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model berhasil dimuat dari penyimpanan lokal.")
    else:
        model = None
        print("Peringatan: File model.joblib tidak ditemukan! Harap jalankan src/train.py terlebih dahulu.")
except Exception as e:
    model = None
    print(f"Gagal memuat model: {e}")

@app.route('/')
def index():
    # Menampilkan antarmuka Dashboard HTML
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint API untuk menerima input dan mengembalikan prediksi polusi PM2.5.
    Menerima JSON berisi: hour, day, latitude, longitude
    """
    if model is None:
        return jsonify({"error": "Model machine learning belum dilatih atau dimuat pada server."}), 500
        
    try:
        data = request.get_json()
        
        # Ekstraksi parameter dari request
        hour = data.get('hour')
        day_of_week = data.get('day')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Validasi kelengkapan parameter
        if None in [hour, day_of_week, latitude, longitude]:
            return jsonify({"error": "Parameter input tidak lengkap! Harap masukkan hour, day, latitude, dan longitude."}), 400
            
        # Konversi ke array numpy 2D sesuai urutan waktu training (hour, day_of_week, latitude, longitude)
        input_data = np.array([[int(hour), int(day_of_week), float(latitude), float(longitude)]])
        
        # Proses prediksi dengan model
        prediction = model.predict(input_data)[0]
        
        # Kembalikan response JSON
        return jsonify({
            "pm25_prediction": round(float(prediction), 2),
            "status": "success"
        })
        
    except ValueError as ve:
        return jsonify({"error": f"Format data input salah: {ve}"}), 400
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan di server: {e}"}), 500

if __name__ == '__main__':
    # Jalankan di host 0.0.0.0 dan port standar Hugging Face Spaces (7860)
    app.run(host='0.0.0.0', port=7860, debug=True)
