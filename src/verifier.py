import os
import re
import json
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _get_secret(name: str):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(name)
    except Exception:
        return None


def evidence_to_text(evidence: List[Dict]) -> str:
    lines = []
    for i, item in enumerate(evidence, start=1):
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        url = item.get("url", "")
        lines.append(f"[{i}] {title}\nSnippet: {snippet}\nURL: {url}")
    return "\n\n".join(lines)


def verify_with_openai(claim: str, evidence: List[Dict]) -> Dict:
    api_key = _get_secret("OPENAI_API_KEY")
    if not api_key:
        return {}

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a strict fact-checking agent.

Verify this claim using only the provided web evidence.

Claim:
{claim}

Web Evidence:
{evidence_to_text(evidence)}

Return only valid JSON with:
{{
  "verdict": "Verified" | "Inaccurate" | "False / No Evidence" | "Needs Review",
  "confidence": number from 0 to 100,
  "correct_fact": "corrected factual statement if available, otherwise empty string",
  "explanation": "short explanation"
}}

Rules:
- Verified: evidence strongly supports the claim.
- Inaccurate: claim has outdated/wrong number/date but evidence gives correct value.
- False / No Evidence: evidence contradicts claim or no reliable evidence supports it.
- Needs Review: evidence is weak or mixed.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You verify factual claims and return strict JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        content = response.choices[0].message.content.strip()
        content = re.sub(r"^```json|```$", "", content).strip()
        data = json.loads(content)
        return data
    except Exception as exc:
        return {
            "verdict": "Needs Review",
            "confidence": 40,
            "correct_fact": "",
            "explanation": f"LLM verification failed, fallback needed: {exc}"
        }


def simple_rule_verification(claim: str, evidence: List[Dict]) -> Dict:
    """Fallback verifier when no OpenAI key exists."""
    if not evidence:
        return {
            "verdict": "False / No Evidence",
            "confidence": 30,
            "correct_fact": "",
            "explanation": "No web evidence found for this claim."
        }

    claim_lower = claim.lower()
    evidence_text = " ".join([
        f"{x.get('title','')} {x.get('snippet','')}" for x in evidence
    ]).lower()

    years = re.findall(r"\b(19|20)\d{2}\b", claim)
    nums = re.findall(r"\d+(\.\d+)?\s?%?", claim)

    year_match = True
    for year in re.findall(r"\b(?:19|20)\d{2}\b", claim):
        if year not in evidence_text:
            year_match = False

    important_words = [
        w for w in re.findall(r"[a-zA-Z]{5,}", claim_lower)
        if w not in {"there", "their", "which", "would", "about", "market", "users"}
    ]
    word_hits = sum(1 for w in important_words if w in evidence_text)
    score = int((word_hits / max(len(important_words), 1)) * 100)

    if score >= 60 and year_match:
        verdict = "Verified"
        confidence = min(85, score)
        explanation = "Several important terms and stated year/figures appear in the retrieved web evidence."
    elif score >= 35:
        verdict = "Needs Review"
        confidence = max(45, score)
        explanation = "Some related evidence was found, but it does not clearly confirm all figures."
    else:
        verdict = "False / No Evidence"
        confidence = 35
        explanation = "Retrieved evidence does not clearly support this claim."

    return {
        "verdict": verdict,
        "confidence": confidence,
        "correct_fact": "",
        "explanation": explanation
    }


def verify_claim(claim: str, evidence: List[Dict]) -> Dict:
    result = verify_with_openai(claim, evidence)
    if result:
        return result
    return simple_rule_verification(claim, evidence)
