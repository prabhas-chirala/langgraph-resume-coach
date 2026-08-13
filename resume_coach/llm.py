from __future__ import annotations

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()


def get_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Get a free key at https://console.groq.com "
            "and put it in .env"
        )
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    return ChatGroq(api_key=api_key, model=model, temperature=0.2)


def parse_json_payload(text: str) -> Any:
    """Extract JSON object/array from model output (tolerates markdown fences)."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
        if not match:
            raise
        return json.loads(match.group(1))


def llm_json(system: str, user: str) -> Any:
    llm = get_llm()
    resp = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    return parse_json_payload(resp.content if isinstance(resp.content, str) else str(resp.content))
