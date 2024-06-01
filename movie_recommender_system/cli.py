import typer

from movie_recommender_system.features.cli import processing_features

app = typer.Typer()

app.command()(processing_features)

def main():
    app()

if __name__ == "__main__":
    app()
