from __future__ import annotations

import argparse
from pathlib import Path

from resume_coach.graph import run_coach


def main() -> int:
    parser = argparse.ArgumentParser(description="LangGraph Resume Coach CLI")
    parser.add_argument("--resume", required=True, help="Path to resume .txt/.md")
    parser.add_argument("--jd", required=True, help="Path to job description .txt/.md")
    args = parser.parse_args()

    resume = Path(args.resume).read_text(encoding="utf-8")
    jd = Path(args.jd).read_text(encoding="utf-8")
    result = run_coach(resume, jd)
    print(result.get("report") or result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
