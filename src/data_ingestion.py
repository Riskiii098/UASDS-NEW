import requests
import pandas as pd
from datetime import datetime
import os

def fetch_and_prepare_data(limit=10000):
    # Menggunakan Open-Meteo Air Quality API (Gratis, Tanpa API Key)
    # Kita ambil data historis PM2.5 untuk wilayah Jakarta dan sekitarnya (sebagai representasi ID)
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    # Ambil data untuk 420 hari terakhir agar mendapatkan ~10.000 baris (per jam)
    params = {
        "latitude": -5.4500,
        "longitude": 105.2667,
        "hourly": "pm2_5",
        "past_days": 420, 
        "timezone": "Asia/Jakarta"
    }
    
    print(f"Mengambil data dari Open-Meteo API...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Open-Meteo mengembalikan dictionary array untuk waktu dan pm2_5
        times = data['hourly']['time']
        pm25_values = data['hourly']['pm2_5']
        
        records = []
        for t, pm in zip(times, pm25_values):
            if pm is not None:  # Abaikan nilai yang kosong
                records.append({
                    'datetime': t,
                    'pm25': pm,
                    'latitude': -5.4500,
                    'longitude': 105.2667,
                    'location': 'Bandar Lampung'
                })
                
        df = pd.DataFrame(records)
        
        if df.empty:
            print("Data yang diambil kosong.")
            return df
            
        # Potong sesuai limit yang diminta user
        df = df.tail(limit)
            
        # Konversi string tanggal menjadi format datetime Pandas
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Ekstrak fitur waktu sebagai input machine learning
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['month'] = df['datetime'].dt.month
        
        # Simpan cache data ke CSV
        cache_path = os.path.join(os.path.dirname(__file__), '..', 'data_polusi_lokal.csv')
        df.to_csv(cache_path, index=False)
        print(f"Berhasil menyimpan {len(df)} baris data bersih ke: {cache_path}")
        
        return df
    else:
        print(f"Gagal mengambil data. Status code: {response.status_code}")
        print(response.text)
        return pd.DataFrame()

if __name__ == "__main__":
    fetch_and_prepare_data()
