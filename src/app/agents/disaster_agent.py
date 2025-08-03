# src/app/agents/disaster_agent.py
import json
from typing import Dict
from openai import OpenAI
from src.app.agents.base_agent import BaseAgent

class DisasterAgent(BaseAgent):
    """Extracts structured data from environmental disaster reports."""

    def __init__(self, base_url: str, model_name: str, temperature: str, api_key: str):
        super().__init__(base_url, model_name, temperature, api_key)
        self.client = OpenAI(base_url=base_url, api_key=self.api_key)

        # ------------- Tool Definition -------------
        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "extract_disaster_info",
                    "description": (
                        "Extract structured info from environmental disaster text (news or reports). "
                        "If a field is not present, omit it."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "disaster_type": {
                                "type": "string",
                                "description": "Type of disaster (e.g. flood, earthquake, wildfire)."
                            },
                            "location": {
                                "type": "string",
                                "description": "Location where the disaster happened (city, region, etc)."
                            },
                            "severity": {
                                "type": "string",
                                "description": "Severity level (low, medium, high, critical)."
                            },
                            "date": {
                                "type": "string",
                                "description": "Date of the disaster (ISO format YYYY-MM-DD)."
                            },
                            "time": {
                                "type": "string",
                                "description": "Time of the disaster (24-hour HH:MM)."
                            },
                            "casualties": {
                                "type": "integer",
                                "description": "Number of deaths or injuries reported (if any)."
                            },
                            "economic_damage": {
                                "type": "string",
                                "description": "Estimated economic loss, if stated (e.g., 1 million USD)."
                            },
                            "note": {
                                "type": "string",
                                "description": "Original text report."
                            }
                        },
                        "required": ["disaster_type", "location"]
                    }
                }
            }
        ]

    def process(self, text: str) -> Dict:
        """Return structured data about the environmental disaster from *text*."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": text}],
            tools=self.tool_definitions,
            temperature=self.temperature,
        )
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
