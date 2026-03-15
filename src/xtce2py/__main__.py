"""Module entrypoint for running xtce2py as a CLI."""

from xtce2py.main import app


def main() -> None:
    """Run the Typer CLI application."""
    app()


if __name__ == "__main__":
    main()
