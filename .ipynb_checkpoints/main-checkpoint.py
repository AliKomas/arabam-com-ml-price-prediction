from fastapi import FastAPI
import joblib
import numpy as np

# 🚗 FastAPI uygulamasını başlat
app = FastAPI(title="Arabam.com Fiyat Tahmin API")

# 📦 Eğitilmiş modeli yükle
model = joblib.load("arabam_fiyat_tahmin_modeli.pkl")

# 🏠 Ana sayfa (test için)
@app.get("/")
def home():
    return {"mesaj": "Arabam.com Fiyat Tahmin API çalışıyor 🚀"}

# 💰 Tahmin endpoint'i
@app.post("/tahmin")
def fiyat_tahmin(motor_hacmi: float, motor_gucu: float, km: int, arac_yasi: int):
    # Kullanıcıdan gelen verileri numpy array'e çevir
    veri = np.array([[motor_hacmi, motor_gucu, km, arac_yasi, yakit_kod]])
    tahmin = model.predict(veri)
    return {"tahmini_fiyat": f"{tahmin[0]:,.0f} ₺"}
