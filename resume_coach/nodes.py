from __future__ import annotations

from .llm import llm_json
from .state import CoachState


def extract_requirements(state: CoachState) -> CoachState:
    jd = state.get("jd", "")
    data = llm_json(
        system=(
            "You extract hiring requirements from job descriptions. "
            "Return ONLY JSON: {\"requirements\": [\"...\"]} with 6-12 concise bullets "
            "(skills, tools, experience). No markdown."
        ),
        user=f"Job description:\n{jd}",
    )
    reqs = data.get("requirements") if isinstance(data, dict) else data
    if not isinstance(reqs, list):
        reqs = []
    return {"requirements": [str(r).strip() for r in reqs if str(r).strip()]}


def score_fit(state: CoachState) -> CoachState:
    resume = state.get("resume", "")
    requirements = state.get("requirements", [])
    data = llm_json(
        system=(
            "You are a technical recruiter scoring resume–JD fit. "
            "Return ONLY JSON with keys: "
            "overall_score (0-100 int), "
            "matched_requirements (string list), "
            "summary (1-2 sentences). No markdown."
        ),
        user=(
            f"Requirements:\n{requirements}\n\n"
            f"Resume:\n{resume}"
        ),
    )
    if not isinstance(data, dict):
        data = {"overall_score": 0, "matched_requirements": [], "summary": "Could not score."}
    score = int(data.get("overall_score", 0))
    score = max(0, min(100, score))
    return {
        "score": {
            "overall_score": score,
            "matched_requirements": data.get("matched_requirements") or [],
            "summary": data.get("summary") or "",
        }
    }


def find_gaps(state: CoachState) -> CoachState:
    resume = state.get("resume", "")
    requirements = state.get("requirements", [])
    matched = (state.get("score") or {}).get("matched_requirements") or []
    data = llm_json(
        system=(
            "Identify gaps between resume evidence and JD requirements. "
            "Return ONLY JSON: {\"gaps\": [\"...\"]} — 3-7 concrete gaps. "
            "Focus on missing tools/projects/impact, not soft fluff."
        ),
        user=(
            f"Requirements:\n{requirements}\n\n"
            f"Already matched:\n{matched}\n\n"
            f"Resume:\n{resume}"
        ),
    )
    gaps = data.get("gaps") if isinstance(data, dict) else data
    if not isinstance(gaps, list):
        gaps = []
    return {"gaps": [str(g).strip() for g in gaps if str(g).strip()]}


def prep_topics(state: CoachState) -> CoachState:
    jd = state.get("jd", "")
    gaps = state.get("gaps", [])
    resume = state.get("resume", "")
    data = llm_json(
        system=(
            "Suggest interview prep topics tailored to this candidate and role. "
            "Return ONLY JSON: {\"prep_topics\": [\"...\"]} with 4-6 specific topics."
        ),
        user=f"JD:\n{jd}\n\nGaps:\n{gaps}\n\nResume:\n{resume[:3000]}",
    )
    topics = data.get("prep_topics") if isinstance(data, dict) else data
    if not isinstance(topics, list):
        topics = []
    return {"prep_topics": [str(t).strip() for t in topics if str(t).strip()]}


def finalize_report(state: CoachState) -> CoachState:
    score = state.get("score") or {}
    gaps = state.get("gaps") or []
    topics = state.get("prep_topics") or []
    requirements = state.get("requirements") or []

    matched = score.get("matched_requirements") or []
    lines = [
        "# Resume Coach Report",
        "",
        f"**Fit score:** {score.get('overall_score', 'N/A')}/100",
        "",
        f"**Summary:** {score.get('summary', '')}",
        "",
        "## Key JD requirements",
    ]
    lines.extend(f"- {r}" for r in requirements)
    lines.extend(["", "## Matched"])
    if matched:
        lines.extend(f"- {m}" for m in matched)
    else:
        lines.append("- None listed")
    lines.extend(["", "## Gaps to close"])
    if gaps:
        lines.extend(f"- {g}" for g in gaps)
    else:
        lines.append("- None")
    lines.extend(["", "## Interview prep"])
    if topics:
        lines.extend(f"- {t}" for t in topics)
    else:
        lines.append("- None")
    return {"report": "\n".join(lines)}
