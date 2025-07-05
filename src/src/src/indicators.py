import talib
import numpy as np

def calculate_indicators(closes):
    closes_array = np.array(closes)
    
    # Calculate indicators
    ema8 = talib.EMA(closes_array, timeperiod=8)
    ema21 = talib.EMA(closes_array, timeperiod=21)
    rsi = talib.RSI(closes_array, timeperiod=14)
    
    # Determine signals
    buy_signal = (ema8[-1] > ema21[-1]) and (rsi[-1] < 30)
    sell_signal = (ema8[-1] < ema21[-1]) and (rsi[-1] > 70)
    
    return {
        'buy_signal': buy_signal,
        'sell_signal': sell_signal,
        'ema8': ema8[-1],
        'ema21': ema21[-1],
        'rsi': rsi[-1]
    }
