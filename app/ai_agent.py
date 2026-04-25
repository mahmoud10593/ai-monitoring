import requests

def analyze_with_openclaw(data):
    try:
        response = requests.post(
            "http://127.0.0.1:18789/v1/chat/completions",
            json={
                "model": "openai/gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
Analyze this website monitoring result:

{data}

Return ONLY JSON:
{{
  "risk": "LOW | MEDIUM | HIGH",
  "reason": "short explanation"
}}
"""
                    }
                ]
            }
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}