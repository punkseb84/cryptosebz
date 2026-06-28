# 🚀 Crypto Scanner V6

Scanner automatico per criptovalute sviluppato in Python.

Analizza il mercato ogni 4 ore utilizzando dati OHLC di Kraken e invia automaticamente su Telegram i migliori setup di trading.

---

# Funzionalità

✅ Analisi di oltre 30 criptovalute

✅ EMA 20 / EMA 50 / EMA 200

✅ Relative Volume (RVOL)

✅ Trend Score

✅ Ranking Score

✅ Swing High

✅ Swing Low

✅ Resistenza più vicina

✅ Supporto più vicino

✅ Breakout confermati

✅ PRE-LONG

✅ LONG SETUP

✅ WATCHLIST

✅ Invio automatico su Telegram

---

# Struttura del progetto

```
crypto-scanner-v6/

├── app.py
├── config.py
├── utils.py
├── indicators.py
├── patterns.py
├── ranking.py
├── signals.py
├── telegram_bot.py
├── scanner.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installazione

Clona il repository

```bash
git clone https://github.com/TUO_USERNAME/crypto-scanner-v6.git

cd crypto-scanner-v6
```

Installa le dipendenze

```bash
pip install -r requirements.txt
```

---

# Variabili d'ambiente

Imposta due variabili:

```
TELEGRAM_BOT_TOKEN

TELEGRAM_CHAT_ID
```

Su Render:

Settings

↓

Environment

↓

Add Environment Variable

---

# Avvio

```bash
python app.py
```

---

# Analisi

Per ogni criptovaluta vengono calcolati:

- EMA20
- EMA50
- EMA200
- Relative Volume
- Trend Score
- Swing High
- Swing Low
- Supporti
- Resistenze
- Ranking Score

---

# LONG SETUP

Un LONG viene generato solamente quando sono soddisfatte tutte le condizioni:

- Trend Score ≥ 2
- Breakout confermato
- RVOL superiore alla soglia
- Breakout sopra la resistenza

---

# PRE-LONG

Una coin entra in PRE-LONG quando:

- Trend Score ≥ 2
- RVOL elevato
- Distanza dalla resistenza ≤ 2%

---

# WATCHLIST

La Watchlist contiene le coin:

- vicine alla resistenza
- ordinate per Score
- senza duplicati rispetto ai PRE-LONG

---

# Trend Score

| Condizione | Punti |
|------------|------:|
| Close > EMA20 | 1 |
| EMA20 > EMA50 | 1 |
| EMA50 > EMA200 | 1 |

Massimo:

```
3/3
```

---

# Ranking Score

Formula:

```
Trend Score
+
RVOL
-
Distanza dalla resistenza
```

I pesi possono essere modificati in:

```
config.py
```

---

# Coin supportate

Il bot monitora 16 coppie USD su Kraken:

- BTC/USD (`XBTUSD`)
- ETH/USD (`ETHUSD`)
- SOL/USD (`SOLUSD`)
- XRP/USD (`XRPUSD`)
- BNB/USD (`BNBUSD`)
- DOGE/USD (`DOGEUSD`)
- ADA/USD (`ADAUSD`)
- TRX/USD (`TRXUSD`)
- LINK/USD (`LINKUSD`)
- AVAX/USD (`AVAXUSD`)
- SUI/USD (`SUIUSD`)
- HYPE/USD (`HYPEUSD`)
- BCH/USD (`BCHUSD`)
- LTC/USD (`LTCUSD`)
- XLM/USD (`XLMUSD`)
- TON/USD (`TONUSD`)

---

# Roadmap

## V6.1

- Swing Low come Stop Loss
- Supporti dinamici

## V6.2

- ATR Stop Loss
- ATR Take Profit

## V6.3

- Trend Daily + Setup 4H

## V6.4

- RSI
- MACD
- Momentum Filter

## V6.5

- Fibonacci
- Breakout Retest

## V7

- Position Sizing
- Risk Management
- Trailing Stop
- Break Even
- Alert avanzati
- Integrazione Exchange
- Auto Trading

---

# Deploy

Compatibile con:

- Render
- Railway
- VPS Linux
- Docker
- GitHub Actions

---

# Licenza

MIT License

---

# Autore

Crypto Scanner V6

Sviluppato con Python e progettato per analisi tecnica automatizzata delle criptovalute.