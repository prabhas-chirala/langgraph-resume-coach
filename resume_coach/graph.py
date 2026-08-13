from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .nodes import extract_requirements, finalize_report, find_gaps, prep_topics, score_fit
from .state import CoachState


def build_graph():
    graph = StateGraph(CoachState)
    graph.add_node("extract_requirements", extract_requirements)
    graph.add_node("score_fit", score_fit)
    graph.add_node("find_gaps", find_gaps)
    graph.add_node("prep_topics", prep_topics)
    graph.add_node("finalize_report", finalize_report)

    graph.add_edge(START, "extract_requirements")
    graph.add_edge("extract_requirements", "score_fit")
    graph.add_edge("score_fit", "find_gaps")
    graph.add_edge("find_gaps", "prep_topics")
    graph.add_edge("prep_topics", "finalize_report")
    graph.add_edge("finalize_report", END)
    return graph.compile()


def run_coach(resume: str, jd: str) -> CoachState:
    app = build_graph()
    return app.invoke({"resume": resume.strip(), "jd": jd.strip()})
