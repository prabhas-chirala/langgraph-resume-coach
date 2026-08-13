from __future__ import annotations

from typing import Any, TypedDict


class CoachState(TypedDict, total=False):
    resume: str
    jd: str
    requirements: list[str]
    score: dict[str, Any]
    gaps: list[str]
    prep_topics: list[str]
    report: str
    error: str
