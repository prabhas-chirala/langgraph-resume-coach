# LangGraph Resume Coach

Multi-agent **LangGraph** pipeline that compares a resume against a job description:

1. **Extract requirements** from the JD  
2. **Score fit** against the resume  
3. **Find gaps** (skills / evidence missing)  
4. **Suggest interview prep** topics  
5. **Write a short coaching report**

Built for Applied AI / GenAI interviews — shows real `StateGraph` nodes, shared state, and tool-style LLM calls (not a single prompt wrapped in Gradio).

## Stack
- LangGraph + LangChain
- Groq (`llama-3.3-70b-versatile`) by default — free tier
- Streamlit UI
- Sample JD + resume included for one-click demo

## Quick start

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# add GROQ_API_KEY=... from https://console.groq.com
streamlit run app.py
```

CLI (no UI):

```bash
python -m resume_coach.cli --resume samples/sample_resume.txt --jd samples/sample_jd.txt
```

## Architecture

```
JD + Resume
    │
    ▼
[extract_requirements] → [score_fit] → [find_gaps] → [prep_topics] → [finalize_report]
    │                         │              │              │               │
    └─────────────────────────┴──────────────┴──────────────┴───────────────┘
                         shared LangGraph state
```

## Why this project
Recruiters ask for LangGraph evidence. This repo is a small, readable multi-agent workflow you can demo and explain end-to-end.
