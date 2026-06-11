<div align="center">

# 📈 Real-Time Stock Market Dashboard

**A professional-grade stock analysis dashboard built with Python, Dash & Plotly**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-4.x-008DE4?style=for-the-badge&logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Deploy](#-deployment)

---

![Dashboard Preview]<img width="1898" height="817" alt="DASHBOARD" src="https://github.com/user-attachments/assets/8a48c4d6-5f9d-4045-9d0e-c32403c2ae65" />

</div>


---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Live Candlestick Chart** | Real-time OHLC data via Yahoo Finance — no API key required |
| 📉 **Bollinger Bands** | 20-period with shaded fill for visual clarity |
| 📈 **EMA Overlays** | EMA 20 and EMA 50 trend lines |
| ⚡ **RSI Indicator** | 14-period with overbought/oversold zones |
| 🔁 **MACD Panel** | Line, signal, and color-coded histogram |
| 💹 **Stats Bar** | Live price, % change, volume, 52W high/low, RSI value |
| 🔍 **Ticker Search** | Search any stock, ETF, or index worldwide |
| ⚡ **Quick Tickers** | One-click access to AAPL, TSLA, NVDA, MSFT, GOOGL, AMZN, META, SPY |
| 🕐 **Multi-Interval** | Switch between 5m, 15m, 1h, and 1d timeframes |
| 🔄 **Auto Refresh** | Dashboard refreshes every 60 seconds automatically |

---

## 🖥 Demo

> Open your browser at **http://localhost:8050** after running the app locally.

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/stock-dashboard.git
cd stock-dashboard
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
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

Visit → **http://localhost:8050** 🎉

---

## 📖 Usage

1. **Search a stock** — type any ticker (e.g. `AAPL`, `BTC-USD`, `^GSPC`) and hit Search
2. **Quick tickers** — click any button in the top-right for instant loading
3. **Change timeframe** — use the interval dropdown (5m / 15m / 1h / 1d)
4. **Read the indicators:**
   - Price touching **BB Upper** → potential overbought zone
   - Price touching **BB Lower** → potential oversold zone
   - **RSI > 70** → overbought signal
   - **RSI < 30** → oversold signal
   - **MACD crosses Signal** → trend reversal signal

---

## 🛠 Tech Stack

| Library | Purpose |
|---|---|
| [Dash](https://dash.plotly.com/) | Reactive Python web framework |
| [Plotly](https://plotly.com/python/) | Interactive charting engine |
| [yfinance](https://github.com/ranaroussi/yfinance) | Yahoo Finance market data |
| [ta](https://github.com/bukosabino/ta) | Technical analysis indicators |
| [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) | UI layout & components |
| [pandas](https://pandas.pydata.org/) | Data manipulation |

---

## 📁 Project Structure

```
stock-dashboard/
├── app.py              # Main application — layout, callbacks, indicators
├── requirements.txt    # Python dependencies
└── README.md           # You are here
```

---

## ☁️ Deployment

### Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repository
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server`
5. Click **Deploy** — your dashboard is live 🌐

> Add `gunicorn` to `requirements.txt` before deploying.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute.

---

<div align="center">

Made with ❤️ and Python

⭐ **Star this repo if you found it useful!**

</div>
