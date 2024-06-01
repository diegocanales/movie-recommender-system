from movie_recommender_system.features.build_features import processing_features
from pathlib import Path
import yaml
import pandas as pd

def processing(data_path: Path = None,
               config_path: Path = None,
               output_path: Path = None) -> None:
    with open(config, "r") as file:
        config = yaml.safe_load(file)
    df = pd.read_csv(data_path)
    df = processing_features(df)
    df.to_csv(output_path, index=False)
