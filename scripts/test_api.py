"""Quick test of OpenAI API availability."""
from openai import OpenAI

client = OpenAI()
try:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Reply with valid JSON containing a greeting field."}],
        response_format={"type": "json_object"},
        max_tokens=50,
    )
    print("SUCCESS:", resp.choices[0].message.content)
except Exception as e:
    print(f"ERROR [{type(e).__name__}]: {e}")
