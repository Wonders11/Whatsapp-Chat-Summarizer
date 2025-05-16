import pandas as pd

def filter_by_date(messages, start_date, end_date):
    df = pd.DataFrame(messages)
    
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Extract only date part for comparison
    df['date_only'] = df['timestamp'].dt.date

    mask = (df['date_only'] >= start_date) & (df['date_only'] <= end_date)
    return df[mask]
