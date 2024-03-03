
import pandas as pd

def compute_rsi(series, window=14):
    """Compute the RSI for a given data series."""
    # Calculate the daily price difference
    delta = series.diff()
    
    # Separate the gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate the rolling average of gains and losses
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    
    # Calculate RS
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def add_rsi_to_dataframe(df):
    df['RSI'] = df.groupby('ticker')['close'].transform(lambda x: compute_rsi(x))
    return df

if __name__ == "__main__":
    data_path = "/path/to/your/csv/file.csv"
    data = pd.read_csv(data_path)
    data_with_rsi = add_rsi_to_dataframe(data)
    print(data_with_rsi.head())
