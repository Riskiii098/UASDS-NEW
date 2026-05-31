import requests
import pandas as pd
from datetime import datetime
import os

def fetch_and_prepare_data(limit=10000):
    url_aq = "https://air-quality-api.open-meteo.com/v1/air-quality"
    url_weather = "https://archive-api.open-meteo.com/v1/archive"
    
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=420)
    
    params = {
        "latitude": -5.4500,
        "longitude": 105.2667,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "timezone": "Asia/Jakarta"
    }
    
    params_aq = params.copy()
    params_aq["hourly"] = "pm2_5"
    
    params_weather = params.copy()
    params_weather["hourly"] = "temperature_2m,relative_humidity_2m,wind_speed_10m"
    
    print(f"Mengambil data Kualitas Udara dari Open-Meteo API...")
    resp_aq = requests.get(url_aq, params=params_aq)
    
    print(f"Mengambil data Cuaca dari Open-Meteo API...")
    resp_weather = requests.get(url_weather, params=params_weather)
    
    if resp_aq.status_code == 200 and resp_weather.status_code == 200:
        data_aq = resp_aq.json()
        data_weather = resp_weather.json()
        
        df_aq = pd.DataFrame({
            'datetime': data_aq['hourly']['time'],
            'pm25': data_aq['hourly']['pm2_5']
        })
        
        df_weather = pd.DataFrame({
            'datetime': data_weather['hourly']['time'],
            'temperature': data_weather['hourly']['temperature_2m'],
            'humidity': data_weather['hourly']['relative_humidity_2m'],
            'wind_speed': data_weather['hourly']['wind_speed_10m']
        })
        
        # Merge both dataframes on datetime
        df = pd.merge(df_aq, df_weather, on='datetime', how='inner')
        
        # Drop missing pm25 values
        df = df.dropna(subset=['pm25'])
        
        # Forward fill weather values if any are missing temporarily
        df = df.fillna(method='ffill')
        
        # Add constant location features
        df['latitude'] = -5.4500
        df['longitude'] = 105.2667
        df['location'] = 'Bandar Lampung'
        
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
        print(f"Gagal mengambil data. Status AQ: {resp_aq.status_code}, Status Cuaca: {resp_weather.status_code}")
        return pd.DataFrame()

if __name__ == "__main__":
    fetch_and_prepare_data()
