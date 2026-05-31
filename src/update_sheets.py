import os
import requests
import pandas as pd

def fetch_recent_data():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    # Mengambil data historis 7 hari terakhir
    params = {
        "latitude": -6.2088,
        "longitude": 106.8456,
        "hourly": "pm2_5",
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "Asia/Jakarta"
    }
    
    print("Mengambil data cuaca terbaru dari Open-Meteo...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        times = data['hourly']['time']
        pm25_values = data['hourly']['pm2_5']
        
        # Header tabel
        records = [['datetime', 'pm25', 'latitude', 'longitude', 'location', 'hour', 'day_of_week', 'month']]
        
        for t, pm in zip(times, pm25_values):
            if pm is not None:
                dt_obj = pd.to_datetime(t)
                records.append([
                    t,
                    pm,
                    -6.2088,
                    106.8456,
                    'Jakarta',
                    dt_obj.hour,
                    dt_obj.dayofweek,
                    dt_obj.month
                ])
        return records
    else:
        print(f"Gagal mengambil data dari API: {response.status_code}")
        return []

def update_google_sheets(records):
    # Menggunakan Webhook URL dari Google Apps Script (Tanpa Kredensial GCP!)
    webhook_url = os.getenv("APPS_SCRIPT_URL")
    
    if not webhook_url:
        print("Peringatan: APPS_SCRIPT_URL belum disetting di GitHub Secrets.")
        return

    try:
        print("Mengirim data ke Google Sheets via Apps Script...")
        # Mengirim data sebagai JSON POST request
        response = requests.post(webhook_url, json=records)
        
        if response.status_code == 200:
            print(f"Berhasil mengupdate {len(records)-1} baris data terbaru ke Google Sheets!")
        else:
            print(f"Gagal update Sheets. Status: {response.status_code}, Response: {response.text}")
            
    except Exception as e:
        print(f"Terjadi kesalahan saat update Google Sheets: {e}")

if __name__ == "__main__":
    new_data = fetch_recent_data()
    if new_data:
        update_google_sheets(new_data)
