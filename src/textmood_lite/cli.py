import sys

from .core import dominant_mood


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: textmood "your text here"')
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    print(dominant_mood(text))


if __name__ == "__main__":
    main()
