# 🚗 Arabam.com Car Price Prediction | ML Project

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)]()
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Model-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

### 🇹🇷 Türkçe Açıklama
Bu proje, Kaggle'da paylaşılan [Arabam.com veri seti](https://www.kaggle.com/datasets/omerdasc/arabam-com-veri) kullanılarak hazırlanmıştır.  
Amaç, bir aracın teknik özelliklerine (motor hacmi, motor gücü, kilometre, araç yaşı, yakıt tipi vb.) göre **tahmini satış fiyatını** makine öğrenmesi modeliyle belirlemektir.

---

## 🧠 Project Overview

**Goal:** Predict the car price based on technical and categorical features.  
**Dataset:** [Arabam.com Dataset on Kaggle](https://www.kaggle.com/datasets/omerdasc/arabam-com-veri)

The workflow covers:
1. Data cleaning & preprocessing  
2. Feature engineering (e.g., Car Age, Fuel Type Encoding)  
3. Model training using **Linear Regression** and **Random Forest**  
4. Model evaluation and comparison  
5. Deployment via **Streamlit Web App**

---

## 🧹 Data Preprocessing

- Removed unnecessary columns (e.g., İlan No, İlan Tarihi)
- Converted text numbers (“300.000 TL”, “150.000 km”) → numeric
- Filled missing values using mean/mode strategy
- Created new column `Araç Yaşı = 2025 - Yıl`
- Encoded categorical variables (Fuel Type → 0=Benzin, 1=Dizel, 2=Hybrid, 3=Elektrik)

---

## 🤖 Model Training

| Model | MAE (₺) | RMSE (₺) | R² |
|--------|----------|-----------|-----|
| Linear Regression | 941,524.26 | 2,082,618.75 | 0.993 |
| **Random Forest Regressor** | **313,763.42** | **1,333,388.98** | **0.997** |

✅ Random Forest achieved the best performance, explaining **~99.7%** of price variance.

---

## ⚙️ Streamlit App

### 🎮 Run the App

```bash
streamlit run app.py
