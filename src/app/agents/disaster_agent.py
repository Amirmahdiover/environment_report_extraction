import json
from openai import OpenAI
import sqlite3
from datetime import datetime

# Example DisasterAgent function (you can use your actual function)
def extract_disaster_info(disaster_type, location, severity=None, date=None, time=None, casualties=None, economic_damage=None, note=None):
    """A placeholder for your disaster info extraction function."""
    # This function is just an example, replace with your actual logic
    return {
        "disaster_type": disaster_type,
        "location": location,
        "severity": severity,
        "date": date,
        "time": time,
        "casualties": casualties,
        "economic_damage": economic_damage,
        "note": note
    }

class DisasterAgent:
    def __init__(self, model_name: str, temperature: float, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.history = []
        self.init_db()
        self.load_history_from_db()

    def save_message_to_db(self, role, content):
        timestamp = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO messages (role, content, timestamp)
            VALUES (?, ?, ?)
        ''', (role, content, timestamp))
        self.conn.commit()

    def load_history_from_db(self):
        self.cursor.execute('''
            SELECT role, content FROM messages
            ORDER BY id DESC
            LIMIT 10
        ''')
        rows = self.cursor.fetchall()

        # Reverse to maintain correct chronological order
        rows.reverse()

        self.history = [{"role": role, "content": content} for role, content in rows]

    def init_db(self, db_path="chat_history.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def process(self, message: str):
        self.history.append({"role": "user", "content": message})
        self.save_message_to_db("user", message)
        """Process the user input and check if function call is needed."""
        # Simulating function calling setup
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.history,
            tools=[self.get_tool_definition()],  # Tools like disaster data extraction
            temperature=self.temperature
        )
        # Check if the response contains a tool call

        message = response.choices[0].message
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # Extract the arguments and call the function
                arguments = json.loads(tool_call.function.arguments)
                
                # Directly call the function with the extracted arguments
                function_response = extract_disaster_info(**arguments)
                
                # Return the raw function response as JSON
                return json.dumps(function_response)  # Raw JSON response
        self.history.append({"role": "assistant", "content": response.choices[0].message.content})
        self.save_message_to_db("assistant", response.choices[0].message.content)
        # If no function call was needed, return a default response
        return response.choices[0].message.content

    def get_tool_definition(self):
        """Tool definition for extracting disaster info."""
        return {
            "type": "function",
            "function": {
                "name": "extract_disaster_info",
                "description": (
                    "Extract structured info from environmental disaster text (news or reports). "
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

