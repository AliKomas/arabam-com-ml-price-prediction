import streamlit as st
import joblib
import numpy as np
import pandas as pd
import pyodbc
import datetime
import matplotlib.pyplot as plt

# ------------------------------------------
# 🎨 Full Navbar Renk Uyumu - Lacivert & Mavi
# ------------------------------------------
st.set_page_config(page_title="Arabam.com ML Tahmin Sistemi", page_icon="🚗", layout="centered")

st.markdown("""
    <style>
    /* 🌈 TAM ARKA PLAN */
    body {
        background: linear-gradient(180deg, #1e3a8a, #2563eb);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(180deg, #1e3a8a, #2563eb);
        color: white;
    }

    /* 🚗 NAVBAR */
    .navbar {
        background: linear-gradient(90deg, #2563eb, #1e3a8a);
        color: white;
        padding: 15px 25px;
        border-radius: 0 0 12px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .navbar h1 {
        color: white;
        font-size: 24px;
        margin: 0;
        display: flex;
        align-items: center;
    }
    .navbar img {
        height: 32px;
        margin-right: 10px;
    }
    .menu {
        display: flex;
        gap: 18px;
    }
    .menu a {
        color: white;
        text-decoration: none;
        font-weight: 500;
        padding: 6px 12px;
        border-radius: 6px;
        transition: 0.3s;
    }
    .menu a:hover {
        background-color: rgba(255,255,255,0.2);
    }

    /* 🧾 KART BLOKLARI */
    div[data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
    }

    /* 🔢 INPUTLAR */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.15);
        color: #111827;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        padding: 8px;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.15);
        color: #111827;
        border-radius: 8px;
    }

    /* 🔘 BUTON */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #1e3a8a);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.6em 1.5em;
        cursor: pointer;
        transition: 0.3s ease;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #60a5fa, #2563eb);
        transform: scale(1.05);
    }

    /* 🔤 BAŞLIKLAR & METİNLER */
    h1, h2, h3, h4, p, label, span, .stMarkdown {
        color: white !important;
    }

    /* 📊 GRAFİK ARKA PLAN */
    canvas {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# HEADER BAR
st.markdown("""
<div class="navbar">
    <h1><img src="https://cdn-icons-png.flaticon.com/512/743/743007.png" /> Arabam.com ML Tahmin</h1>
    <div class="menu">
        <a href="#kullanici">Kullanıcı</a>
        <a href="#tahmin">Tahmin</a>
        <a href="#admin">Admin</a>
    </div>
</div>
""", unsafe_allow_html=True)



# ------------------------------------------
# ⚙️ Model ve Veritabanı Bağlantısı
# ------------------------------------------
model = joblib.load("arabam_fiyat_tahmin_modeli.pkl")

conn_str = (
    "Driver={SQL Server};"
    "Server=DESKTOP-7NNG9GJ\SQLEXPRESS;"   # 💡 kendi server adını yaz
    "Database=ArabamML;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

admin_list = ["alikomas@gmail.com", "admin@arabam.com"]

# ------------------------------------------
# 1️⃣ Kullanıcı Girişi
# ------------------------------------------

st.markdown('<div id="kullanici"></div>', unsafe_allow_html=True)


st.title("🚗 Arabam.com Fiyat Tahmin ve Kayıt Sistemi")

st.divider()
st.subheader("👤 Kullanıcı Girişi")

adsoyad = st.text_input("Ad Soyad", placeholder="Ali Komaş")
email = st.text_input("E-posta", placeholder="alikomas@gmail.com")

if "giris" not in st.session_state:
    st.session_state["giris"] = False

if st.button("🔐 Giriş Yap / Kaydol"):
    if adsoyad.strip() == "" or email.strip() == "":
        st.error("⚠️ Lütfen tüm bilgileri girin.")
    else:
        cursor.execute("SELECT COUNT(*) FROM Kullanici WHERE Email = ?", (email,))
        (var_mi,) = cursor.fetchone()
        if var_mi == 0:
            cursor.execute("INSERT INTO Kullanici (AdSoyad, Email) VALUES (?, ?)", (adsoyad, email))
            conn.commit()
            st.success(f"✅ Yeni kullanıcı oluşturuldu: {adsoyad}")
        else:
            st.info(f"👋 Hoş geldiniz tekrar, {adsoyad.split()[0]}!")
        st.session_state["giris"] = True

# ------------------------------------------
# 2️⃣ Araç Özellikleri + Tahmin
# ------------------------------------------
st.markdown('<div id="tahmin"></div>', unsafe_allow_html=True)


st.divider()
st.subheader("🚙 Araç Özellikleri")

if not st.session_state["giris"]:
    st.warning("⚠️ Lütfen önce giriş yapın.")
else:
    col1, col2 = st.columns(2)
    with col1:
        motor_hacmi = st.number_input("Motor Hacmi (cc)", 800, 6000, 1600)
        yakit_tipi = st.selectbox("Yakıt Tipi", ["Benzin", "Dizel", "Hybrid", "Elektrik"])
    with col2:
        motor_gucu = st.number_input("Motor Gücü (hp)", 50, 500, 120)
        km = st.number_input("Kilometre", 0, 500000, 100000)

    arac_yasi = st.slider("Araç Yaşı", 0, 50, 5, format="%d yıl")
    yakit_map = {"Benzin": 0, "Dizel": 1, "Hybrid": 2, "Elektrik": 3}
    yakit_kod = yakit_map[yakit_tipi]

    if st.button("📈 Tahmin Et ve Kaydet"):
        veri = np.array([[motor_hacmi, motor_gucu, km, arac_yasi, yakit_kod]])
        tahmin = model.predict(veri)[0]
        st.success(f"💰 Tahmini Fiyat: {tahmin:,.0f} ₺")

        cursor.execute("""
            INSERT INTO Tahminler (AdSoyad, Email, MotorHacmi, MotorGucu, Km, AracYasi, YakitTipi, Tahmin, TahminTarihi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (adsoyad, email, motor_hacmi, motor_gucu, km, arac_yasi, yakit_tipi, tahmin, datetime.datetime.now()))
        conn.commit()
        st.info("✅ Tahmin veritabanına kaydedildi.")

    st.markdown("### 📋 Geçmiş Tahminlerin")
    df_user = pd.read_sql("SELECT * FROM Tahminler WHERE Email = ? ORDER BY TahminTarihi DESC", conn, params=[email])
    if len(df_user) > 0:
        st.dataframe(df_user, use_container_width=True)
    else:
        st.write("Henüz tahmin geçmişin bulunmuyor.")

# ------------------------------------------
# 3️⃣ Admin Panel (Grafikler)
# ------------------------------------------
st.markdown('<div id="admin"></div>', unsafe_allow_html=True)



st.divider()
if email in admin_list:
    st.subheader("🧑‍💼 Admin Paneli — Genel Görünüm")
    df = pd.read_sql("SELECT * FROM Tahminler", conn)
    st.dataframe(df, use_container_width=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        yakit_df = df.groupby("YakitTipi")["Tahmin"].mean().reset_index()
        plt.figure(figsize=(5,3))
        plt.bar(yakit_df["YakitTipi"], yakit_df["Tahmin"], color="#2563eb")
        plt.title("Yakıt Tipine Göre Ortalama Fiyat")
        st.pyplot(plt)

    with col_a2:
        yas_df = df.groupby("AracYasi")["Tahmin"].mean().reset_index()
        plt.figure(figsize=(5,3))
        plt.plot(yas_df["AracYasi"], yas_df["Tahmin"], marker='o', color="#6366f1")
        plt.title("Araç Yaşına Göre Ortalama Fiyat")
        st.pyplot(plt)
else:
    st.info("🔒 Admin değilsen yalnızca kendi tahminlerini görebilirsin.")
