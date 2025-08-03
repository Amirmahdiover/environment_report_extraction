# src/app/agents/base_agent.py
from abc import ABC

class BaseAgent(ABC):
    base_url: str
    model_name: str
    temperature: float
    api_key: str

    def __init__(self, base_url, model_name, temperature, api_key):
        super().__init__()
        self.base_url = base_url
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key
        self.client = None

    def process(self):
        raise NotImplementedError
