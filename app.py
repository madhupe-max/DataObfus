from __future__ import annotations

import re
from typing import Dict, Tuple

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="DataObfus API", version="0.1.0")


class ObfuscateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw input text to obfuscate")


class ObfuscateResponse(BaseModel):
    obfuscated_text: str
    replacements: Dict[str, int]


PII_PATTERNS: Dict[str, str] = {
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "phone": r"\b(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
}


def obfuscate_text(text: str) -> Tuple[str, Dict[str, int]]:
    counts: Dict[str, int] = {}
    output = text

    for label, pattern in PII_PATTERNS.items():
        token = f"[{label.upper()}]"
        output, count = re.subn(pattern, token, output)
        counts[label] = count

    return output, counts


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/obfuscate", response_model=ObfuscateResponse)
def obfuscate(request: ObfuscateRequest) -> ObfuscateResponse:
    obfuscated, counts = obfuscate_text(request.text)
    return ObfuscateResponse(obfuscated_text=obfuscated, replacements=counts)
