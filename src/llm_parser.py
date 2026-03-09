import json

class LLMParser:
    """
    Acts as the Layer 3 Command Center interface.
    Currently uses simple rule-based matching as a mock for an LLM to quickly test the Layer 1 Mutability loop.
    Can be swapped out for real LLM API calls later.
    """
    def __init__(self):
        # A simple keyword to JSON map for testing
        self.mock_rules = {
            "heavy gravity": '{"GRAVITY": 1.5, "FLAP_STRENGTH": -10.0}',
            "moon gravity": '{"GRAVITY": 0.2, "FLAP_STRENGTH": -5.0}',
            "fast pipes": '{"PIPE_SPEED": 8.0, "PIPE_SPAWN_FREQUENCY": 60}',
            "slow pipes": '{"PIPE_SPEED": 1.0}',
            "tiny pipes": '{"PIPE_WIDTH": 20}',
            "big bird": '{"BIRD_WIDTH": 60, "BIRD_HEIGHT": 60}',
            "reset": '{"GRAVITY": 0.5, "FLAP_STRENGTH": -8.0, "PIPE_SPEED": 3.0, "PIPE_WIDTH": 60, "PIPE_SPAWN_FREQUENCY": 100, "BIRD_WIDTH": 30, "BIRD_HEIGHT": 30}'
        }

    def parse_command(self, user_text: str) -> dict:
        """
        Parses natural language and returns a dictionary of settings changes.
        """
        user_text = user_text.lower().strip()
        
        # In a real implementation, we would send `user_text` to an LLM here, 
        # asking it to return ONLY a JSON string mapping text to our settings.py values.
        
        # Mock matching
        for keyword, json_str in self.mock_rules.items():
            if keyword in user_text:
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    print(f"Error decoding mock JSON for {keyword}")
                    return {}
        
        # If no match, return empty dict meaning no changes
        print(f"LLMParser: Command '{user_text}' not understood by mock parser.")
        return {}
