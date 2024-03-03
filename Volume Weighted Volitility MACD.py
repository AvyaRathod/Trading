
import pandas as pd
import numpy as np

def f_kalman_filter_updated(_src, length, ac):
    AC = 1 if ac else 0
    out = [0.0] * len(_src)
    K = [0.0] * len(_src)
    
    for i in range(1, len(_src)):
        prev_out = out[i-1] if not np.isnan(out[i-1]) else _src[i]
        prev_K = K[i-1] if not np.isnan(K[i-1]) else 0.0
        
        src = _src[i] + (_src[i] - prev_out)
        out[i] = prev_out + prev_K * (src - prev_out) + AC * (prev_K * (src - np.mean(_src[max(0, i-length+1):i+1])))
        K[i] = abs(src - out[i]) / (abs(src - out[i]) + np.std(_src[max(0, i-length+1):i+1]) * length) if np.std(_src[max(0, i-length+1):i+1]) != 0 else 0.0
    
    return out

def f_HVWMA(src, volume, length):
    pi = np.pi
    c = [0]
    
    for i in range(1, len(src)):
        c.append(c[i-1] + 1 if c[i-1] == length else c[i-1] + 1)
    
    h_ = [volume[i] * (0.54 - 0.46 * np.cos((2 * pi * c[i]) / length)) for i in range(len(src))]
    hwma = [np.sum(np.array(h_[max(0, i-length+1):i+1]) * np.array(src[max(0, i-length+1):i+1])) / np.sum(h_[max(0, i-length+1):i+1]) for i in range(len(src))]
    
    return hwma

def VWV_MACD(data):
    src_input = data['close'] + data['low'] + data['high'] / 3  # hlc3
    period = 10
    usevwap = True
    Hlength = 200
    fastperiod = 12
    slowperiod = 26
    signalperiod = 9
    kalman = True
    klength = 14
    ac = True

    # VWAP or HVWMA
    if usevwap:
        data['vwap'] = (data['volume'] * (data['high'] + data['low'] + data['close']) / 3).cumsum() / data['volume'].cumsum()
    else:
        data['vwap'] = f_HVWMA(src_input, data['volume'], Hlength)

    # Volume Weighted Volatility (VWV)
    totalVolume = data['volume'].rolling(window=period).sum()
    data['vwv_'] = np.sqrt(data['volume'] * (src_input - data['vwap'])**2 / totalVolume)
    data['vwv'] = f_kalman_filter_updated(data['vwv_'].tolist(), klength, ac)

    # MACD calculations
    data['fastMA'] = data['vwv'].ewm(span=fastperiod).mean()
    data['slowMA'] = data['vwv'].ewm(span=slowperiod).mean()
    data['macd'] = data['fastMA'] - data['slowMA']
    data['signal'] = data['macd'].ewm(span=signalperiod).mean()
    data['VWV_MACD'] = data['macd'] - data['signal']

    return data

