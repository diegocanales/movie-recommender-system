import pandas as pd
from pathlib import Path

def create_dataset(movie_data_path: Path = None, credits_data_path: Path = None, output_path: Path = None):
    print(f"Loading data from {movie_data_path}")
    df_movies = pd.read_csv(movie_data_path)
    print(f"Loading data from {credits_data_path}")
    df_credits = pd.read_csv(credits_data_path)
    print("Merging data")
    df = df_movies.merge(df_credits, on="title")
    print("Remove missing values")
    df = df.dropna()
    df.to_csv(output_path, index=False)
