
import pandas as pd

def adjust_time(file_path):
    # Load the preprocessed dataset
    data = pd.read_csv(file_path)

    # Convert 'Date' and 'Time' columns to a single datetime object
    data['Datetime'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str))

    # Round the time to the nearest minute
    data['Datetime'] = data['Datetime'].dt.round('T')

    # Extract the adjusted time component
    data['Time'] = data['Datetime'].dt.time

    # Define market opening and closing times
    opening_time = pd.Timestamp('09:15:00').time()
    closing_time = pd.Timestamp('15:30:00').time()

    # Adjust times outside the market operation range
    data.loc[data['Time'] < opening_time, 'Time'] = opening_time
    data.loc[data['Time'] > closing_time, 'Time'] = closing_time

    # Drop the 'Datetime' column used for processing
    data.drop(columns=['Datetime'], inplace=True)

    # Save the adjusted data to the specified output path
    data.to_csv(output_path, index=False)
    print(f"Time adjusted and data saved to {output_path}")

if __name__ == "__main__":
    file_path = input("Enter the path to the preprocessed CSV file: ")
    output_path = input("Enter the path for saving the time-adjusted data: ")
    adjust_time(file_path, output_path)
