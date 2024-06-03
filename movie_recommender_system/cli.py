import typer

from movie_recommender_system.features.cli import processing
from movie_recommender_system.data.make_dataset import create_dataset
from movie_recommender_system.models.train_model import train_model

app = typer.Typer()

app.command()(create_dataset)
app.command()(processing)
app.command()(train_model)


def main():
    app()

if __name__ == "__main__":
    app()
