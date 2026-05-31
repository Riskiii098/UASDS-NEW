import os
import requests
import pandas as pd

def fetch_recent_data():
    url_aq = "https://air-quality-api.open-meteo.com/v1/air-quality"
    url_weather = "https://api.open-meteo.com/v1/forecast"
    
    # Mengambil data historis 7 hari terakhir
    params = {
        "latitude": -5.4500,
        "longitude": 105.2667,
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "Asia/Jakarta"
    }
    
    params_aq = params.copy()
    params_aq["hourly"] = "pm2_5"
    
    params_weather = params.copy()
    params_weather["hourly"] = "temperature_2m,relative_humidity_2m,wind_speed_10m"
    
    print("Mengambil data Kualitas Udara terbaru dari Open-Meteo...")
    resp_aq = requests.get(url_aq, params=params_aq)
    
    print("Mengambil data Cuaca terbaru dari Open-Meteo...")
    resp_weather = requests.get(url_weather, params=params_weather)
    
    if resp_aq.status_code == 200 and resp_weather.status_code == 200:
        data_aq = resp_aq.json()
        data_weather = resp_weather.json()
        
        # Open-Meteo returns hourly arrays
        times_aq = data_aq['hourly']['time']
        pm25_values = data_aq['hourly']['pm2_5']
        
        times_weather = data_weather['hourly']['time']
        temp_values = data_weather['hourly']['temperature_2m']
        hum_values = data_weather['hourly']['relative_humidity_2m']
        wind_values = data_weather['hourly']['wind_speed_10m']
        
        # Buat dictionary untuk weather lookup by time
        weather_dict = {}
        for i, t in enumerate(times_weather):
            weather_dict[t] = {
                'temp': temp_values[i],
                'hum': hum_values[i],
                'wind': wind_values[i]
            }
        
        # Header tabel
        records = [['datetime', 'pm25', 'latitude', 'longitude', 'location', 'hour', 'day_of_week', 'month', 'temperature', 'humidity', 'wind_speed']]
        
        for i, t in enumerate(times_aq):
            pm = pm25_values[i]
            if pm is not None and t in weather_dict:
                w = weather_dict[t]
                if w['temp'] is not None:  # pastikan data cuaca ada
                    dt_obj = pd.to_datetime(t)
                    records.append([
                        t,
                        pm,
                        -5.4500,
                        105.2667,
                        'Bandar Lampung',
                        dt_obj.hour,
                        dt_obj.dayofweek,
                        dt_obj.month,
                        w['temp'],
                        w['hum'],
                        w['wind']
                    ])
        return records
    else:
        print(f"Gagal mengambil data dari API: AQ={resp_aq.status_code}, Weather={resp_weather.status_code}")
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
