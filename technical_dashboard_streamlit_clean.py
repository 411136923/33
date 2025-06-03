import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("📈 技術指標儀表板（pandas-ta）")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [c.lower() for c in df.columns]
    df.rename(columns={"aapl.close": "close", "aapl.high": "high", "aapl.low": "low", "date": "time"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"])
    return df

df = load_data()
df["RSI"] = ta.rsi(df["close"], length=14)
macd = ta.macd(df["close"])
df["MACD"] = macd["MACD_12_26_9"]
df["SIGNAL"] = macd["MACDs_12_26_9"]
bb = ta.bbands(df["close"], length=20)
df["BB_UPPER"] = bb["BBU_20_2.0"]
df["BB_MIDDLE"] = bb["BBM_20_2.0"]
df["BB_LOWER"] = bb["BBL_20_2.0"]

option = st.sidebar.selectbox("選擇指標", ["RSI", "MACD", "布林通道"])

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

# 價格圖
fig.add_trace(go.Scatter(x=df["time"], y=df["close"], name="收盤價", line=dict(color="black")), row=1, col=1)

if option == "RSI":
    fig.add_trace(go.Scatter(x=df["time"], y=df["RSI"], name="RSI", line=dict(color="purple")), row=2, col=1)
elif option == "MACD":
    fig.add_trace(go.Scatter(x=df["time"], y=df["MACD"], name="MACD", line=dict(color="blue")), row=2, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=df["SIGNAL"], name="SIGNAL", line=dict(color="orange")), row=2, col=1)
elif option == "布林通道":
    fig.add_trace(go.Scatter(x=df["time"], y=df["BB_UPPER"], name="上軌", line=dict(color="gray")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=df["BB_MIDDLE"], name="中軌", line=dict(color="blue")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=df["BB_LOWER"], name="下軌", line=dict(color="gray")), row=1, col=1)

fig.update_layout(height=600, title_text=f"{option} 技術分析圖", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)