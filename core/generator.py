import google.generativeai as genai
from flyn.core.prompts import build_prompt

def generate_command(user_input, config):
    api_key = config.get("api_key") or config.get("gemini_api_key")
    model_name = config.get("model", "gemini-2.0-flash")
    os_name = config.get("os", "windows").lower()
    temperature = config.get("temperature", 0.4)

    if not api_key:
        return {
            "command": "",
            "explanation": "Missing Gemini API key"
        }

    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        return {"command": "", "explanation": f"Gemini init error: {e}"}

    # Build prompt with OS conditioning
    prompt = build_prompt(
        instruction=user_input,
        os_name=os_name
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        text = (response.text or "").strip()
    except Exception as e:
        return {"command": "", "explanation": f"Gemini error: {e}"}

    # --- Output parsing ---
    command = ""
    explanation = ""

    for raw in text.splitlines():
        line = raw.strip()
        if line.lower().startswith("command:"):
            command = line.split(":", 1)[1].strip()
        elif line.lower().startswith("explanation:"):
            explanation = line.split(":", 1)[1].strip()

    return {
        "command": command,
        "explanation": explanation
    }
