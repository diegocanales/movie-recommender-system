from movie_recommender_system.models.model import MovieRecommender
from pathlib import Path
import pandas as pd
import pickle

def save_model(model: MovieRecommender, output_path: Path = None):
    with open(output_path, "wb") as f:
        pickle.dump(model, f)


def train_model(data_path: Path = None, output_path: Path = None):
    df_processed = pd.read_csv(data_path)
    model = MovieRecommender()
    model.fit(df_processed)
    save_model(model, output_path)
