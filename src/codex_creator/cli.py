from __future__ import annotations

import argparse
import json

from .executor import Executor
from .planner import plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Codex Creator Agent")
    parser.add_argument("prompt", help="Natural-language creation request")
    parser.add_argument("--plan-only", action="store_true", help="Only print the planned job")
    args = parser.parse_args()

    job = plan(args.prompt)
    if args.plan_only:
        print(json.dumps(job.to_dict(), indent=2, ensure_ascii=False))
        return 0

    result = Executor().run(job)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

