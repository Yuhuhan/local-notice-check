"""Hugging Face Space entrypoint.

Application code lives in the ``app`` package; this file only starts it.
"""

from app.cli import main
from app.server import app

__all__ = ["app", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
