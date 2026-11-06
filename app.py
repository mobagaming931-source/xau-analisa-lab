# app.py - Jantung AI nya
from flask import Flask, jsonify
import requests
import pandas as pd

app = Flask(__name__)

# WARNING: Ini bukan financial advice. High risk!
def get_xau_price():
    # pakai API gratis, contoh TwelveData
    # ganti dengan API key pian
    url = "https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=5min&apikey=DEMO"
    data = requests.get(url).json()
    return data

def analisa_ai(candles):
    # Hitung indikator sederhana
    df = pd.DataFrame(candles)
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    df['rsi'] = hitung_rsi(df['close'])
    df['atr'] = hitung_atr(df)

    harga = df['close'].iloc[-1]
    atr = df['atr'].iloc[-1]

    # LOGIKA AI - HARUS 3 SYARAT
    if df['ema20'].iloc[-1] > df['ema50'].iloc[-1] and df['rsi'].iloc[-1] > 50 and df['rsi'].iloc[-1] < 70:
        signal = "BUY IDE"
        sl = harga - (atr * 1.5)
        tp1 = harga + (atr * 1.5)
        tp2 = harga + (atr * 3)
    elif df['ema20'].iloc[-1] < df['ema50'].iloc[-1] and df['rsi'].iloc[-1] < 50:
        signal = "SELL IDE"
        sl = harga + (atr * 1.5)
        tp1 = harga - (atr * 1.5)
        tp2 = harga - (atr * 3)
    else:
        signal = "WAIT / NO TRADE"

    return {
        "harga": harga,
        "signal": signal,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "alasan": "EMA20 vs EMA50 + RSI + ATR"
    }

@app.route('/api/signal')
def signal():
    # return analisa_ai(...)
    return jsonify({"disclaimer": "Edukasi saja, bukan ajakan trading. Forex beresiko tinggi."})
