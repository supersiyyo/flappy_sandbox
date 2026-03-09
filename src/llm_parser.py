import json
import os

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class LLMParser:
    """
    Parses natural language commands from the Game Director into JSON settings changes.
    Uses 'google-genai' to dynamically interpret prompts. If no API key is set, falls back to a mock parser.
    """
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = 'gemini-2.5-flash'
            print("✅ LLMParser initialized with Gemini API.")
        else:
            self.client = None
            print("⚠️ WARNING: GEMINI_API_KEY not found or google-genai missing. Using basic mock parser.")
            print("   To enable semantic AI adjustments, set GEMINI_API_KEY in your environment.")

        # Real LLM System Prompt
        self.system_prompt = """
You are the Game Master for a Flappy Bird game. The user will give you a natural language command to change the game's physics or rules.
You must analyze the command and output a JSON object containing ONLY the settings variables to update and their new numeric values.
Available settings and their default values:
- GRAVITY (float, default: 0.5)
- FLAP_STRENGTH (float, default: -8.0)
- MAX_VELOCITY (float, default: 10.0)
- PIPE_SPEED (float, default: 3.0)
- PIPE_WIDTH (int, default: 60)
- PIPE_GAP_SIZE (int, default: 150)
- PIPE_SPAWN_FREQUENCY (int, default: 100, frames between spawns)
- BIRD_WIDTH (int, default: 30)
- BIRD_HEIGHT (int, default: 30)

Respond strictly with ONLY a JSON dictionary of the updated variables. If the requested change is impossible or invalid, return an empty dictionary {}.
Example input: "make the pipes super fast"
Example output: {"PIPE_SPEED": 8.0}
        """

        # Fallback Mock Rules
        self.mock_rules = {
            "heavy gravity": '{"GRAVITY": 1.5, "FLAP_STRENGTH": -10.0}',
            "fast pipes": '{"PIPE_SPEED": 8.0, "PIPE_SPAWN_FREQUENCY": 60}'
        }

    def parse_command(self, user_text: str) -> dict:
        user_text = user_text.strip()
        
        if self.client:
            print(f"🧠 Parsing via Gemini: '{user_text}'...")
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_text,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        response_mime_type="application/json",
                        temperature=0.1
                    ),
                )
                
                result_text = response.text.strip()
                # Clean up potential markdown formatting code blocks
                if result_text.startswith("```json"):
                    result_text = result_text[7:-3].strip()
                elif result_text.startswith("```"):
                    result_text = result_text[3:-3].strip()
                
                updates = json.loads(result_text)
                return updates
            except Exception as e:
                print(f"❌ Error communicating with LLM: {e}")
                return {}
        else:
            # Fallback mock logic
            for keyword, json_str in self.mock_rules.items():
                if keyword in user_text.lower():
                    return json.loads(json_str)
            print(f"Mock Parser: Cannot understand '{user_text}'. (Missing API Key for real interpretation)")
            return {}
