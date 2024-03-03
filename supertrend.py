import pandas as pd
import numpy as np

def calculate_supertrend(df, period=7, multiplier=3):
    """
    Calculates the Supertrend indicator for a DataFrame that contains OHLCV data.

    Args:
    df (pandas.DataFrame): The input DataFrame containing the stock data. It should contain the columns 'open', 'high', 'low', and 'close'.
    period (int): The period to use for the ATR calculation. Default is 7.
    multiplier (float): The multiplier to use for the ATR calculation. Default is 3.

    Returns:
    pandas.DataFrame: A new DataFrame that contains the input data and an additional column with the Supertrend values.

    """

    # Calculate the ATR
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)

    atr = true_range.rolling(period).mean()

    # Calculate the Upper and Lower Bands
    upper_band = (df['high'] + df['low']) / 2 + (multiplier * atr)
    lower_band = (df['high'] + df['low']) / 2 - (multiplier * atr)

    # Calculate the Supertrend
    supertrend = pd.Series(0.0, index=df.index)
    supertrend[0] = np.nan

    for i in range(1, len(df)):
        if df['close'][i] > upper_band[i-1]:
            supertrend[i] = lower_band[i]
        elif df['close'][i] < lower_band[i-1]:
            supertrend[i] = upper_band[i]
        else:
            supertrend[i] = supertrend[i-1] if df['close'][i-1] < supertrend[i-1] else lower_band[i] if df['close'][i] > lower_band[i] else upper_band[i]

    # Add the Supertrend to the DataFrame
    df['supertrend'] = supertrend

    return df
