import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import joblib
from dotenv import load_dotenv

# Load environment variables (contoh untuk DagsHub tracking URI & credential)
load_dotenv()

def train_model():
    # Inisialisasi MLflow Tracking (Hubungkan ke DagsHub via environment variable)
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "")
    if mlflow_tracking_uri:
        mlflow.set_tracking_uri(mlflow_tracking_uri)
    
    # Baca data cache (5000 baris dari OpenAQ)
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data_polusi_lokal.csv')
    if not os.path.exists(data_path):
        print(f"Data belum ada di {data_path}. Jalankan data_ingestion.py terlebih dahulu.")
        return
        
    df = pd.read_csv(data_path)
    if df.empty:
        print("Data CSV kosong, training tidak dapat dilanjutkan.")
        return
        
    print(f"Memulai training model dengan {len(df)} baris data...")
    
    # Tentukan Fitur (X) dan Target (y)
    features = ['hour', 'day_of_week', 'latitude', 'longitude']
    target = 'pm25'
    
    X = df[features]
    y = df[target]
    
    # Split data (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Mulai eksperimen di MLflow
    mlflow.set_experiment("Prediksi-Kualitas-Udara-PM25")
    
    with mlflow.start_run():
        n_estimators = 50  # Dibatasi agar lebih cepat dan hemat RAM
        
        # Inisialisasi dan Train model
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        
        # Lakukan prediksi pada data test
        y_pred = model.predict(X_test)
        
        # Evaluasi model
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Evaluasi Model:")
        print(f"MAE: {mae:.2f}")
        print(f"MSE: {mse:.2f}")
        print(f"R-Squared (R2): {r2:.2f}")
        
        # Logging ke MLflow (Parameter dan Metrik)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("features", features)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)
        
        # Logging Model Artifact ke MLflow
        mlflow.sklearn.log_model(model, "random_forest_pm25")
        
        # Simpan Model Lokal (.joblib) sebagai cadangan untuk Flask
        model_path = os.path.join(os.path.dirname(__file__), '..', 'model.joblib')
        joblib.dump(model, model_path)
        print(f"Model berhasil disimpan ke: {model_path}")

if __name__ == "__main__":
    train_model()
