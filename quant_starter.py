import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sayfa Ayarı
st.set_page_config(page_title="Quant Mersin Live", layout="wide")
st.title("📈 Quant-Mersin: Canlı Veri Analiz Paneli")

# Kenar Çubuğu (Sidebar)
st.sidebar.header("Ayarlar")
ticker = st.sidebar.text_input("Hisse Kodu (Örn: SISE.IS)", "SISE.IS")
period = st.sidebar.selectbox("Dönem", ["1mo", "6mo", "1y"])

# Veriyi Çek
try:
    data = yf.download(ticker, period=period, interval="1d")
    
    if not data.empty:
        # EMA Hesapla
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
        
        # Son Durum Sinyali (İşte burası geleceği/şimdiği söyler)
        last_price = data['Close'].iloc[-1].item()
        last_ema20 = data['EMA20'].iloc[-1].item()
        last_ema50 = data['EMA50'].iloc[-1].item()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Son Fiyat", f"{last_price:.2f} TL")
        
        if last_ema20 > last_ema50:
            st.success("🟢 GÜNCEL DURUM: YÜKSELİŞ TRENDİ (ALIM BÖLGESİ)")
        else:
            st.error("🔴 GÜNCEL DURUM: DÜŞÜŞ TRENDİ (SATIŞ BÖLGESİ)")

        # Grafik Çizimi
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data['Close'], label='Fiyat', color='black', alpha=0.3)
        ax.plot(data['EMA20'], label='EMA20 (Hızlı)', color='blue')
        ax.plot(data['EMA50'], label='EMA50 (Yavaş)', color='red')
        ax.legend()
        st.pyplot(fig)
        
    else:
        st.warning("Veri bulunamadı, lütfen kodu kontrol edin.")

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")