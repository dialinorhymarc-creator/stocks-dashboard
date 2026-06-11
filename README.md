# 📈 Real-Time Stock Market Dashboard

An interactive stock dashboard with live data, Bollinger Bands, RSI, MACD, and EMA overlays — built with Python, Dash, and Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Dash](https://img.shields.io/badge/Dash-2.17-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🗂 Project Structure

```
stock-dashboard/
├── app.py              ← Main application (all logic + layout)
├── requirements.txt    ← Dependencies
└── README.md
```

---

## ⚙️ Setup — Step by Step

### Step 1 — Clone / create the project folder
```bash
mkdir stock-dashboard
cd stock-dashboard
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
python app.py
```

Open your browser at → **http://localhost:8050**

---

## 🚀 Features

| Feature | Details |
|---|---|
| Live Data | Fetched via `yfinance` — no API key needed |
| Candlestick Chart | OHLC candles with color-coded up/down |
| Bollinger Bands | 20-period, 2 std dev with fill |
| EMA 20 / EMA 50 | Trend overlays |
| RSI (14) | With overbought/oversold lines |
| MACD | Line, signal, and histogram |
| Stats Bar | Price, change %, volume, 52W high/low, RSI |
| Quick Tickers | One-click AAPL, TSLA, NVDA, etc. |
| Auto Refresh | Every 60 seconds |
| Intervals | 5m, 15m, 1h, 1d |

---

## 📦 Tech Stack

- **[Dash](https://dash.plotly.com/)** — Reactive Python web framework
- **[Plotly](https://plotly.com/python/)** — Interactive charting
- **[yfinance](https://github.com/ranaroussi/yfinance)** — Yahoo Finance data
- **[pandas-ta](https://github.com/twopirllc/pandas-ta)** — Technical analysis indicators
- **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)** — UI components

---

## 🌐 Deploy to Render (Free)

1. Push this project to a GitHub repo
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server`
5. Deploy — your dashboard is live 🎉

> Add `gunicorn` to `requirements.txt` for deployment.

---

## 📸 Screenshots

> Add screenshots of your running dashboard here for GitHub impact!

---

## 📄 License

MIT — feel free to use and modify.