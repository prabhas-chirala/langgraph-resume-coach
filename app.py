from __future__ import annotations

from pathlib import Path

import streamlit as st
from pypdf import PdfReader

from resume_coach.graph import run_coach

ROOT = Path(__file__).resolve().parent
SAMPLES = ROOT / "samples"


def read_pdf(uploaded) -> str:
    reader = PdfReader(uploaded)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


st.set_page_config(page_title="LangGraph Resume Coach", page_icon="🧠", layout="wide")
st.title("LangGraph Resume Coach")
st.caption("Multi-agent pipeline: extract → score → gaps → prep → report")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Resume PDF (optional)", type=["pdf"])
    resume_text = st.text_area(
        "Resume text",
        height=280,
        value=(SAMPLES / "sample_resume.txt").read_text(encoding="utf-8"),
    )
    if resume_file is not None:
        resume_text = read_pdf(resume_file)

with col2:
    jd_text = st.text_area(
        "Job description",
        height=320,
        value=(SAMPLES / "sample_jd.txt").read_text(encoding="utf-8"),
    )

if st.button("Run LangGraph coach", type="primary"):
    if not resume_text.strip() or not jd_text.strip():
        st.error("Paste both resume and JD.")
    else:
        with st.spinner("Running agent graph..."):
            try:
                result = run_coach(resume_text, jd_text)
            except Exception as e:
                st.error(str(e))
            else:
                score = (result.get("score") or {}).get("overall_score")
                st.metric("Fit score", f"{score}/100" if score is not None else "N/A")
                st.markdown(result.get("report") or "")
                with st.expander("Raw state"):
                    st.json(
                        {
                            "requirements": result.get("requirements"),
                            "score": result.get("score"),
                            "gaps": result.get("gaps"),
                            "prep_topics": result.get("prep_topics"),
                        }
                    )
