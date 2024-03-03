
import pandas as pd

def compute_macd(data, ticker, short_window=12, long_window=26, signal_window=9):
    # Filter data for the given ticker
    ticker_data = data[data['ticker'] == ticker].copy()
    
    # Compute short and long EMAs
    ticker_data['EMA12'] = ticker_data['close'].ewm(span=short_window, adjust=False).mean()
    ticker_data['EMA26'] = ticker_data['close'].ewm(span=long_window, adjust=False).mean()
    
    # Compute MACD
    ticker_data['MACD'] = ticker_data['EMA12'] - ticker_data['EMA26']
    
    # Compute Signal Line
    ticker_data['Signal_Line'] = ticker_data['MACD'].ewm(span=signal_window, adjust=False).mean()
    
    return ticker_data

if __name__ == "__main__":
    file_path = input("Enter the path to the preprocessed CSV file: ")
    data = pd.read_csv(file_path, parse_dates=True, index_col='Datetime')
    ticker = input("Enter the ticker for which you want to compute MACD (e.g., 'RELIANCE-EQ'): ")
    result = compute_macd(data, ticker)
    output_path = input("Enter the path for saving the MACD data: ")
    result.to_csv(output_path)
    print(f"MACD computed and saved to {output_path}")
