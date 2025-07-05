# Enhanced with shorting, risk management, websockets, and visualization
import numpy as np
import talib
from binance.client import Client
from binance import ThreadedWebsocketManager
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configuration
PAIRS = ['SUIUSDT', 'HBARUSDT', 'ADAUSDT', 'XLMUSDT', 'XRPUSDT', 'ENAUSDT']
TIMEFRAME = Client.KLINE_INTERVAL_5MINUTE
RISK_PERCENT = 0.5  # 0.5% per trade
REWARD_RATIO = 1.5   # 1.5:1 profit/risk

class ScalpingBot:
    def __init__(self):
        self.client = Client(api_key, api_secret)
        self.twm = ThreadedWebsocketManager(api_key, api_secret)
        self.open_positions = {}
        self.fig, self.ax = plt.subplots(2, 1, figsize=(12, 8))
        
    def start(self):
        # Historical data first
        for pair in PAIRS:
            self.analyze_pair(pair)
        
        # Real-time websocket
        self.twm.start()
        for pair in PAIRS:
            self.twm.start_kline_socket(
                callback=self.handle_socket_message,
                symbol=pair,
                interval=TIMEFRAME
            )
        self.twm.start()
        
        # Start visualization
        ani = FuncAnimation(self.fig, self.update_chart, interval=30000)
        plt.show()

    def analyze_pair(self, pair):
        klines = self.client.get_klines(symbol=pair, interval=TIMEFRAME, limit=100)
        closes = np.array([float(x[4]) for x in klines])
        volumes = np.array([float(x[5]) for x in klines])
        
        # Calculate indicators
        ema8 = talib.EMA(closes, 8)
        ema21 = talib.EMA(closes, 21)
        rsi6 = talib.RSI(closes, 6)
        
        # Detect signals
        self.check_signals(pair, closes, ema8, ema21, rsi6, volumes)
        
        # Update visualization
        self.plot_data(pair, closes, ema8, ema21, rsi6)

    def handle_socket_message(self, msg):
        if msg['e'] == 'kline' and msg['k']['x']:  # Candle closed
            pair = msg['s']
            closes = np.array([float(msg['k']['c'])])
            # Get more history if needed and process
            
    def check_signals(self, pair, closes, ema8, ema21, rsi6, volumes):
        current_vol = volumes[-1]
        avg_vol = np.mean(volumes[-20:])
        price_change_pct = ((closes[-1] - closes[-2]) / closes[-2]) * 100
        
        # LONG Conditions
        if (ema8[-1] > ema21[-1] and ema8[-2] <= ema21[-2] and
            rsi6[-1] < 35 and
            current_vol > 2.5 * avg_vol and
            price_change_pct > self.get_threshold(pair)):
            
            stop_loss = closes[-1] * (1 - RISK_PERCENT/100)
            take_profit = closes[-1] * (1 + (RISK_PERCENT/100)*REWARD_RATIO)
            
            self.send_alert(
                f"🚀 LONG {pair}\n"
                f"Entry: {closes[-1]:.4f}\n"
                f"SL: {stop_loss:.4f} | TP: {take_profit:.4f}\n"
                f"RSI: {rsi6[-1]:.1f} | Vol: {current_vol/avg_vol:.1f}x"
            )
            self.open_positions[pair] = ('long', closes[-1], stop_loss, take_profit)
        
        # SHORT Conditions (reverse logic)
        elif (ema8[-1] < ema21[-1] and ema8[-2] >= ema21[-2] and
              rsi6[-1] > 65 and
              current_vol > 2.5 * avg_vol and
              price_change_pct < -self.get_threshold(pair)):
            
            stop_loss = closes[-1] * (1 + RISK_PERCENT/100)
            take_profit = closes[-1] * (1 - (RISK_PERCENT/100)*REWARD_RATIO)
            
            self.send_alert(
                f"🔻 SHORT {pair}\n"
                f"Entry: {closes[-1]:.4f}\n"
                f"SL: {stop_loss:.4f} | TP: {take_profit:.4f}\n"
                f"RSI: {rsi6[-1]:.1f} | Vol: {current_vol/avg_vol:.1f}x"
            )
            self.open_positions[pair] = ('short', closes[-1], stop_loss, take_profit)

    def plot_data(self, pair, closes, ema8, ema21, rsi):
        self.ax[0].clear()
        self.ax[1].clear()
        
        # Price chart
        self.ax[0].plot(closes, label='Price', color='blue')
        self.ax[0].plot(ema8, label='EMA 8', color='orange', linestyle='--')
        self.ax[0].plot(ema21, label='EMA 21', color='green', linestyle='--')
        self.ax[0].set_title(f'{pair} Price and Indicators')
        self.ax[0].legend()
        
        # RSI chart
        self.ax[1].plot(rsi, label='RSI 6', color='purple')
        self.ax[1].axhline(70, color='red', linestyle='--')
        self.ax[1].axhline(30, color='green', linestyle='--')
        self.ax[1].legend()
        
        plt.tight_layout()

    def update_chart(self, frame):
        # Refresh data periodically
        for pair in PAIRS[:1]:  # Just show first pair for demo
            self.analyze_pair(pair)

    def get_threshold(self, pair):
        thresholds = {
            'SUIUSDT': 0.5, 'HBARUSDT': 0.3, 'ADAUSDT': 0.4,
            'XLMUSDT': 0.25, 'XRPUSDT': 0.35, 'ENAUSDT': 0.6
        }
        return thresholds.get(pair, 0.4)

    def send_alert(self, message):
        # Implement your actual notification (Telegram, Email, etc.)
        print(f"\nALERT: {message}")
        # Example Telegram integration:
        # requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
        #              data={'chat_id': CHAT_ID, 'text': message})

if __name__ == "__main__":
    bot = ScalpingBot()
    bot.start()
