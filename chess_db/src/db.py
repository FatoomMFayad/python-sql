import pandas as pd
import sqlite3 as sq
import os

#load file
chess_url = 'https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view'
chess_url='https://drive.google.com/uc?id=' + chess_url.split('/')[-2]
def load_data(url: str, local_path: str)-> pd.DataFrame:
    if os.path.exists(local_path):
        print(f'Loading from cache: {local_path}')
        return pd.read_csv(local_path)
    print(f'Downloading from {url}...')
    df = pd.read_csv(url)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path, index=False)
    print(f'Saved to {local_path}')
    return df

chess_df = load_data(chess_url, 'chess_db/data/raw/chess_games.csv')


