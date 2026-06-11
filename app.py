import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf
import ta

# ── App Init ────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    title="Stock Dashboard",
)
server = app.server  # for deployment (gunicorn)

# ── Helpers ─────────────────────────────────────────────────────────────────

INTERVALS = ["1d", "1h", "15m", "5m"]
PERIODS    = {"1d": "5d", "1h": "60d", "15m": "5d", "5m": "2d"}

POPULAR = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "SPY"]


def fetch_data(ticker: str, interval: str) -> pd.DataFrame:
    period = PERIODS.get(interval, "60d")
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df.empty:
        return df
    df.columns = df.columns.droplevel(1) if isinstance(df.columns, pd.MultiIndex) else df.columns
    df.index = pd.to_datetime(df.index)

    # ── Technical Indicators ────────────────────────────────────────────────
    close = df["Close"].squeeze()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_mid"]   = bb.bollinger_mavg()
    df["BB_lower"] = bb.bollinger_lband()

    # RSI
    df["RSI"] = ta.momentum.RSIIndicator(close, window=14).rsi()

    # MACD
    macd = ta.trend.MACD(close, window_slow=26, window_fast=12, window_sign=9)
    df["MACD"]        = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["MACD_hist"]   = macd.macd_diff()

    # EMA 20 / EMA 50
    df["EMA20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
    df["EMA50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()

    return df


def build_figure(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.55, 0.22, 0.23],
        subplot_titles=(f"{ticker} Price + Bollinger Bands", "RSI (14)", "MACD"),
    )

    # ── Row 1 : Candlestick + BB + EMA ──────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        name="Price",
        increasing_line_color="#00e5ff",
        decreasing_line_color="#ff1744",
    ), row=1, col=1)

    for col, color, name in [
        ("BB_upper", "rgba(255,214,0,0.6)",  "BB Upper"),
        ("BB_mid",   "rgba(255,214,0,0.3)",  "BB Mid"),
        ("BB_lower", "rgba(255,214,0,0.6)",  "BB Lower"),
        ("EMA20",    "rgba(0,229,255,0.8)",  "EMA 20"),
        ("EMA50",    "rgba(255,111,0,0.8)",  "EMA 50"),
    ]:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[col], name=name,
                line=dict(color=color, width=1.2),
                mode="lines",
            ), row=1, col=1)

    # BB fill
    if "BB_upper" in df.columns and "BB_lower" in df.columns:
        fig.add_trace(go.Scatter(
            x=pd.concat([df.index.to_series(), df.index.to_series()[::-1]]),
            y=pd.concat([df["BB_upper"], df["BB_lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(255,214,0,0.05)",
            line=dict(color="rgba(255,255,255,0)"),
            name="BB Band",
            showlegend=False,
        ), row=1, col=1)

    # ── Row 2 : RSI ──────────────────────────────────────────────────────────
    if "RSI" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI"], name="RSI",
            line=dict(color="#e040fb", width=1.5),
        ), row=2, col=1)
        for level, color in [(70, "rgba(255,23,68,0.4)"), (30, "rgba(0,229,255,0.4)")]:
            fig.add_hline(y=level, line_dash="dot", line_color=color, row=2, col=1)

    # ── Row 3 : MACD ─────────────────────────────────────────────────────────
    if "MACD" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD"], name="MACD",
            line=dict(color="#00e5ff", width=1.5),
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD_signal"], name="Signal",
            line=dict(color="#ff6d00", width=1.2),
        ), row=3, col=1)
        colors = ["#00e5ff" if v >= 0 else "#ff1744" for v in df["MACD_hist"].fillna(0)]
        fig.add_trace(go.Bar(
            x=df.index, y=df["MACD_hist"], name="Histogram",
            marker_color=colors, opacity=0.7,
        ), row=3, col=1)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#0d0d0d",
        font=dict(family="Inter, sans-serif", color="#e0e0e0"),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.02, x=0),
        margin=dict(l=10, r=10, t=60, b=10),
        height=820,
    )
    fig.update_xaxes(showgrid=True, gridcolor="#1e1e1e", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#1e1e1e", zeroline=False)
    return fig


def stat_card(label: str, value: str, color: str = "#00e5ff") -> dbc.Col:
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.P(label, className="text-muted mb-1", style={"fontSize": "0.75rem"}),
                html.H5(value, style={"color": color, "fontWeight": 700}),
            ])
        ], color="dark", outline=True),
        xs=6, sm=4, md=2,
    )


# ── Layout ───────────────────────────────────────────────────────────────────
app.layout = dbc.Container(fluid=True, children=[
    # Header
    dbc.Row(dbc.Col(html.H2(
        "📈 Real-Time Stock Dashboard",
        className="text-center py-3",
        style={"color": "#00e5ff", "letterSpacing": "2px"},
    ))),

    # Controls
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(id="ticker-input", placeholder="Enter ticker (e.g. AAPL)",
                          value="AAPL", type="text",
                          style={"backgroundColor": "#1a1a1a", "color": "#fff", "borderColor": "#333"}),
                dbc.Button("Search", id="search-btn", color="info", n_clicks=0),
            ]),
        ], md=4),
        dbc.Col([
            dcc.Dropdown(
                id="interval-dropdown",
                options=[{"label": i, "value": i} for i in INTERVALS],
                value="1d",
                clearable=False,
                style={"backgroundColor": "#1a1a1a", "color": "#000"},
            ),
        ], md=2),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button(t, id=f"quick-{t}", color="secondary", size="sm", n_clicks=0)
                for t in POPULAR
            ], className="flex-wrap"),
        ], md=6),
    ], className="mb-3 g-2"),

    # Stats row
    dbc.Row(id="stats-row", className="mb-3 g-2"),

    # Chart
    dbc.Row(dbc.Col(dcc.Graph(id="main-chart", config={"displayModeBar": True}))),

    # Auto-refresh every 60 s
    dcc.Interval(id="auto-refresh", interval=60_000, n_intervals=0),

    # Hidden store for current ticker
    dcc.Store(id="current-ticker", data="AAPL"),
], style={"backgroundColor": "#0d0d0d", "minHeight": "100vh"})


# ── Callbacks ────────────────────────────────────────────────────────────────

# Sync ticker from quick-buttons
@app.callback(
    Output("current-ticker", "data"),
    Output("ticker-input", "value"),
    [Input("search-btn", "n_clicks")] +
    [Input(f"quick-{t}", "n_clicks") for t in POPULAR],
    [State("ticker-input", "value"), State("current-ticker", "data")],
    prevent_initial_call=True,
)
def update_ticker(search_clicks, *args):
    quick_clicks = args[:len(POPULAR)]
    ticker_value, current = args[len(POPULAR):]

    ctx = dash.callback_context
    if not ctx.triggered:
        return current, ticker_value

    prop = ctx.triggered[0]["prop_id"]
    if prop == "search-btn.n_clicks":
        return (ticker_value or "AAPL").upper(), (ticker_value or "AAPL").upper()

    for t in POPULAR:
        if prop == f"quick-{t}.n_clicks":
            return t, t

    return current, ticker_value


# Update chart + stats
@app.callback(
    Output("main-chart", "figure"),
    Output("stats-row", "children"),
    Input("current-ticker", "data"),
    Input("interval-dropdown", "value"),
    Input("auto-refresh", "n_intervals"),
)
def update_chart(ticker, interval, _):
    df = fetch_data(ticker, interval)

    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            template="plotly_dark", paper_bgcolor="#0d0d0d",
            annotations=[dict(text=f"No data for '{ticker}'", showarrow=False,
                              font=dict(size=20, color="#ff1744"))],
        )
        return empty_fig, []

    # ── Stats ────────────────────────────────────────────────────────────────
    close   = float(df["Close"].iloc[-1])
    prev    = float(df["Close"].iloc[-2]) if len(df) > 1 else close
    chg     = close - prev
    chg_pct = (chg / prev) * 100
    vol     = float(df["Volume"].iloc[-1])
    high52  = float(df["High"].max())
    low52   = float(df["Low"].min())
    rsi_val = float(df["RSI"].iloc[-1]) if "RSI" in df.columns else float("nan")

    chg_color = "#00e5ff" if chg >= 0 else "#ff1744"

    cards = [
        stat_card("Price",   f"${close:.2f}",                "#ffffff"),
        stat_card("Change",  f"{chg:+.2f} ({chg_pct:+.2f}%)", chg_color),
        stat_card("Volume",  f"{int(vol):,}",                "#b0bec5"),
        stat_card("52W High",f"${high52:.2f}",              "#69f0ae"),
        stat_card("52W Low", f"${low52:.2f}",               "#ff6d00"),
        stat_card("RSI",     f"{rsi_val:.1f}" if not pd.isna(rsi_val) else "—",
                  "#e040fb"),
    ]

    return build_figure(df, ticker), cards


if __name__ == "__main__":
    app.run(debug=True, port=8050)