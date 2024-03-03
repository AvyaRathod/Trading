
import pandas as pd

def preprocess_data(file_path):
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Drop the redundant columns
    data.drop(columns=['Unnamed: 0', 'index'], inplace=True)

    # Remove duplicate rows
    data.drop_duplicates(inplace=True)
    
    # Convert the 'Datetime' column to a datetime object with timezone
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data['Datetime'] = data['Datetime'].dt.round('T')

    # Create separate 'Date' and 'Time' columns and remove timezone from 'Time'
    data['Date'] = data['Datetime'].dt.date
    data['Time'] = data['Datetime'].dt.time

    # Define market opening and closing times
    opening_time = pd.Timestamp('09:15:00').time()
    closing_time = pd.Timestamp('15:30:00').time()

    # Adjust times outside the market operation range
    data.loc[data['Time'] < opening_time, 'Time'] = opening_time
    data.loc[data['Time'] > closing_time, 'Time'] = closing_time

    data.drop(columns=['Datetime'], inplace=True)

    # Reorder columns for better readability
    data = data[['Date', 'Time', 'open', 'high', 'low', 'close', 'volume', 'ticker']]

    # Sort data based on Date, Time and then ticker
    data.sort_values(by=['Date', 'Time', 'ticker'], inplace=True)
    
    return data

if __name__ == "__main__":
    file_path = input("Enter the path to the CSV file: ")
    processed_data = preprocess_data(file_path)
    output_path = input("Enter the path for saving the preprocessed data: ")
    processed_data.to_csv(output_path, index=False)
    print(f"Data preprocessed and saved to {output_path}")
