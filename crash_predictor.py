import streamlit as st
import random

st.set_page_config(page_title="Dự đoán Crash Game", page_icon="🎯")

st.title("🎯 Tool Dự Đoán Hệ Số Game Crash")
st.markdown("Dự đoán hệ số nổ tiếp theo dựa trên lịch sử gần nhất. Mô hình đơn giản nhưng vui vẻ 😉")

# Nhập lịch sử hệ số
crash_input = st.text_input(
    "🔢 Nhập lịch sử hệ số nổ (cách nhau bằng dấu phẩy):",
    value="1.35, 1.02, 1.10, 1.05, 1.87, 2.91, 1.12, 1.01, 1.30, 1.05"
)
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# ======== CẤU HÌNH DRIVER =========
CHROME_DRIVER_PATH = "chromedriver"  # Đường dẫn tới chromedriver.exe nếu trên Windows
URL = "https://i.hit.club"

# ======== LẤY DỮ LIỆU HỆ SỐ BAY ========
def get_he_so_list():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    driver.get(URL)
    time.sleep(10)  # Chờ trang tải xong

    try:
        he_so_elements = driver.find_elements(By.CLASS_NAME, 'his-item')
        he_so_list = []
        for elem in he_so_elements:
            text = elem.text.replace("x", "").strip()
            try:
                he_so_list.append(float(text))
            except:
                continue
        driver.quit()
        return he_so_list
    except Exception as e:
        driver.quit()
        st.error(f"Lỗi khi lấy dữ liệu: {e}")
        return []

# ======== DỰ ĐOÁN HỆ SỐ TIẾP THEO ========
def predict_next(data):
    if len(data) < 10:
        return "Không đủ dữ liệu"

    X, y = [], []
    for i in range(len(data) - 3):
        X.append(data[i:i+3])
        y.append(data[i+3])
    model = RandomForestRegressor()
    model.fit(X, y)
    pred = model.predict([data[-3:]])
    return round(pred[0], 2)

# ======== GIAO DIỆN STREAMLIT ========
st.set_page_config(page_title="Tool Dự Đoán Bay HITCLUB", layout="centered")
st.title("🚀 Tool Dự Đoán Hệ Số Bay – i.hit.club")

if st.button("🔄 Quét & Dự đoán hệ số"):
    data = get_he_so_list()
    if data:
        st.subheader("📊 Lịch sử hệ số bay")
        st.line_chart(data[::-1])  # Đảo ngược để hiển thị từ cũ đến mới
        du_doan = predict_next(data)
        st.success(f"🧠 Dự đoán hệ số tiếp theo: **{du_doan}x**")
    else:
        st.error("Không lấy được dữ liệu.")
