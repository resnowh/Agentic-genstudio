from __future__ import annotations

import argparse

from .web import serve


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Agentic GenStudio web app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()
    serve(host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

