# import sys
import typer

from textmood_lite.core import analyze, dominant_mood

# from .core import dominant_mood

app = typer.Typer(help="Detect the mood of any text.")

# def main() -> None:
#     if len(sys.argv) < 2:
#         print('Usage: textmood "your text here"')
#         sys.exit(1)
#     text = " ".join(sys.argv[1:])
#     print(dominant_mood(text))


@app.command()
def detect(
    text: str = typer.Argument(..., help="The text to analyze"),
    detailed: bool = typer.Option(
        False, "--detailed", "-d", help="Show all mood scores"
    ),
):
    """Detect the dominant mood of the given text."""
    if detailed:
        scores = analyze(text)
        for mood, score in scores.items():
            typer.echo(f"{mood}: {score}")
    else:
        mood = dominant_mood(text)
        typer.echo(mood)


def main():
    app()


if __name__ == "__main__":
    main()
