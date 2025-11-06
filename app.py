import streamlit as st
import joblib
import numpy as np

model = joblib.load("arabam_fiyat_tahmin_modeli.pkl")

st.title("🚗 Arabam.com Fiyat Tahmin Uygulaması")

motor_hacmi = st.number_input("Motor Hacmi (cc)", 800, 6000, 1600)
motor_gucu = st.number_input("Motor Gücü (hp)", 50, 500, 120)
km = st.number_input("Kilometre", 0, 500000, 100000)
arac_yasi = st.number_input("Araç Yaşı", 0, 50, 5)
yakıt_tipi = st.selectbox("Yakıt Tipi", ["Benzin", "Dizel", "Hybrid", "Elektrik"])

# Encoding
if yakıt_tipi == "Benzin":
    yakit_kod = 0
elif yakıt_tipi == "Dizel":
    yakit_kod = 1
elif yakıt_tipi == "Hybrid":
    yakit_kod = 2
else:
    yakit_kod = 3

if st.button("Tahmin Et"):
    veri = np.array([[motor_hacmi, motor_gucu, km, arac_yasi, yakit_kod]])
    tahmin = model.predict(veri)
    st.success(f"Tahmini Fiyat: {tahmin[0]:,.0f} ₺")
