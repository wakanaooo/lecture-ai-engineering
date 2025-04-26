import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# CSVファイル名
CSV_FILE = "health_log.csv"

st.set_page_config(page_title="健康管理アプリ", layout="wide")
st.title("🍀 健康管理アプリ")

# ============================================
# 日付
# ============================================
st.sidebar.header("📅 日付")
date = st.sidebar.date_input("今日", value=datetime.date.today())

# ============================================
# 睡眠時間
# ============================================
st.header("🛌 睡眠")
sleep_hours = st.slider("睡眠時間 (時間)", 0.0, 12.0, 7.0, 0.5)
ideal_sleep = 8.0
sleep_diff = sleep_hours - ideal_sleep
if sleep_diff < 0:
    st.error(f"理想より{abs(sleep_diff)}時間少ないです。")
elif sleep_diff > 0:
    st.success(f"理想より{sleep_diff}時間多く寝ました！")
else:
    st.info("理想的な睡眠時間です！")

# ============================================
# 運動
# ============================================
st.header("🏃‍♀️ 運動")
exercise = st.radio("運動しましたか？", ("はい", "いいえ"))
exercise_type = "なし"
exercise_minutes = 0

if exercise == "はい":
    exercise_type = st.selectbox("運動の種類", ["ウォーキング", "ランニング", "筋トレ", "ヨガ", "水泳", "その他"])
    exercise_minutes = st.number_input("運動時間 (分)", min_value=0, max_value=300, value=30)
    calories_burned = round(exercise_minutes * 5.0, 1)  # 簡易的な計算
    st.write(f"推定消費カロリー：{calories_burned} kcal")

# ============================================
# 食事
# ============================================
st.header("🍱 食事")

meal_status = {}
meal_fullness = {}
meal_icons = {"朝食": "🌞", "昼食": "🍱", "夕食": "🌙"}

for meal in ["朝食", "昼食", "夕食"]:
    st.subheader(meal)
    meal_status[meal] = st.radio(f"{meal}を食べましたか？", ("はい", "いいえ"), key=meal)
    if meal_status[meal] == "はい":
        st.markdown(f"{meal_icons[meal]} {meal}をしっかり食べましたね！")
        meal_fullness[meal] = st.slider(f"{meal}の満腹度", 0, 100, 80, key=meal + "_full")
    else:
        meal_fullness[meal] = 0

# ============================================
# ボタン
# ============================================
st.header("✅ 完了")
if st.button("押す"):
    new_data = pd.DataFrame([{
        "日付": date,
        "睡眠時間": sleep_hours,
        "運動": exercise,
        "運動種類": exercise_type,
        "運動時間": exercise_minutes,
        "朝食": meal_status["朝食"],
        "朝食満腹度": meal_fullness["朝食"],
        "昼食": meal_status["昼食"],
        "昼食満腹度": meal_fullness["昼食"],
        "夕食": meal_status["夕食"],
        "夕食満腹度": meal_fullness["夕食"]
    }])

    try:
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data

    df.to_csv(CSV_FILE, index=False)
    st.success("データを保存しました！")

    st.balloons()

# ============================================
# 集計
# ============================================
st.header("📈 集計")

fake_data = pd.DataFrame({
    "日付": pd.date_range(end=datetime.date.today(), periods=7),
    "睡眠時間": np.random.uniform(5, 9, 7),
    "運動時間": np.random.randint(0, 60, 7),
    "朝食満腹度": np.random.randint(50, 100, 7),
})

st.line_chart(fake_data.set_index("日付")[["睡眠時間", "運動時間"]])
st.bar_chart(fake_data.set_index("日付")[["朝食満腹度"]])
