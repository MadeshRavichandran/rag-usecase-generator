import json
import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def safe_json_parse(text: str):
    if not text or not text.strip():
        raise ValueError("Empty LLM response")

    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).strip()
    stack = []
    start = None

    for i, ch in enumerate(text):
        if ch == "{":
            if not stack:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    candidate = text[start:i + 1]
                    return json.loads(candidate)

    raise ValueError("No valid JSON object found")


def add_usecase_ids(output_json):
    if "useCases" not in output_json:
        return output_json

    for idx, uc in enumerate(output_json["useCases"], start=1):
        uc.setdefault("id", f"UC-{idx:02d}")

    return output_json


def generate_use_cases(query, context_chunks):
    context = "\n\n".join(c["text"] for c in context_chunks)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a test-case generation system.\n"
                    "Rules:\n"
                    "1. Use ONLY the provided context.\n"
                    "2. Do NOT invent features.\n"
                    "3. Output ONLY a valid JSON object.\n"
                    "4. No explanations, no markdown.\n"
                )
            },
            {
                "role": "user",
                "content": f"CONTEXT:\n{context}\n\nQUERY:\n{query}"
            }
        ],
        temperature=0
    )

    raw_text = response.choices[0].message.content

    try:
        parsed = json.loads(raw_text)
    except Exception:
        print("\n JSON not clean, applying safe parser...\n")
        parsed = safe_json_parse(raw_text)

    return add_usecase_ids(parsed)
