import json
import os

from openai import OpenAI

from app.schemas.generation import GenerationResult

# OpenAI() reads OPENAI_API_KEY from env (set in .env or docker-compose)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = (
    "You generate Instagram carousel slides. "
    "Return ONLY valid JSON with schema: {\"slides\":[{\"order\":1,\"title\":\"...\",\"body\":\"...\",\"footer\":\"...\"}]}. "
    "No markdown, no comments."
)


def build_prompt(
    source_text: str,
    language: str,
    slides_count: int,
    style_hint: str | None,
) -> str:
    style_part = f"\nStyle hint:\n{style_hint}\n" if style_hint else ""
    return (
        f"Language: {language}\n"
        f"Slides count: {slides_count}\n"
        f"{style_part}"
        f"Source text:\n{source_text}\n\n"
        "Constraints:\n"
        "- title <= 80 chars\n"
        "- body <= 420 chars\n"
        "- keep text short so it fits 1080x1350\n"
        "- order must be 1..N\n"
        "Return JSON only."
    )


def generate_slides(
    source_text: str,
    language: str,
    slides_count: int,
    style_hint: str | None,
    model: str,
) -> GenerationResult:
    prompt = build_prompt(source_text, language, slides_count, style_hint)

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    content = resp.choices[0].message.content or ""
    # strip possible markdown code block
    if content.strip().startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    data = json.loads(content.strip())
    return GenerationResult.model_validate(data)
