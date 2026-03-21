import requests
import json
import config
from memory_handler import MemoryHandler

class Brain:
    def __init__(self):
        self.url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL
        self.memory = MemoryHandler()

    def process(self, text):
        """
        Sends user text to Ollama and returns a structured JSON response.
        """
        print(f"Thinking about: {text}")
        
        # 1. Get Memory Context
        memory_context = self.memory.get_memory_string()

        system_prompt = f"""
        You are Aura, a helpful AI assistant running locally.
        You can execute local commands.
        
        {memory_context}
        
        Your ONLY output must be a valid JSON object. Do not include any other text or markdown.
        
        IMPORTANT: Normalize app names to their standard English names (e.g., "calc" -> "calculator", "whtasapp" -> "whatsapp").
        
        Available Actions:
        - open_app: Open a local application (parameter: app name like "notepad", "chrome", "calculator")
        - close_app: Close a local application (parameter: app name like "notepad", "chrome", "calculator")
        - email: Draft and send an email (parameter: {{"recipient": "email_address", "topic": "short_description"}})
        - whatsapp_msg: Send a WhatsApp message (parameter: {{"contact": "full name like Mohan Dharun", "message": "content"}})
        - whatsapp_call: Make a WhatsApp voice call (parameter: {{"contact": "full name"}})
        - play_music: Play a song on Spotify (parameter: {{"song": "song name or 'popular'"}})
        - news: Get top news headlines (parameter: {{"category": "topic e.g. 'crypto', 'tech', 'india'", "limit": 3}})
        - create_folder: Create a new folder (parameter: {{"name": "folder name", "path": "specific path or 'desktop'/'documents' (optional)"}})
        - delete_folder: Delete a folder (parameter: {{"name": "folder name", "path": "specific path or 'desktop'/'documents' (optional)"}})
        - volume_control: Control volume (parameter: {{"action": "set/mute/unmute", "value": "0-100 (optional)"}})
        - power_control: System power (parameter: {{"action": "shutdown/restart/sleep"}})
        - screenshot: Take a screenshot (parameter: null)
        - google_search: Google Search (parameter: {{"query": "search term"}})
        - youtube_play: Play on YouTube (parameter: {{"query": "video name"}})
        - weather: Check weather (parameter: {{"location": "city name or null"}})
        - definition: Define a term (parameter: {{"term": "word to define"}})
        - translate: Translate text (parameter: {{"text": "text to translate", "target": "language (e.g. spanish, french)"}})
        - system_info: Get system status (parameter: null)
        - remember: Save a detail about the user (parameter: {{"key": "what it is (e.g. name, birthday)", "value": "the detail"}})
        - clipboard: Get recent clipboard history (parameter: null)
        - timer: Set a timer or alarm (parameter: {{"duration_minutes": 10, "message": "reminder text"}})
        - calendar: Read or create calendar events (parameter: {{"action": "read" or "create", "time": "e.g., tomorrow 3 PM (for create)", "summary": "event description (for create)"}})
        - chat: General conversation (parameter: null)
        
        JSON Format:
        {{
            "action": "action_name",
            "parameter": "parameter_value_or_object_or_null",
            "response": "What you want to say primarily to the user"
        }}
        
        Example:
        User: "Open Notepad"
        Output: {{ "action": "open_app", "parameter": "notepad", "response": "Opening Notepad for you." }}

        User: "My name is Anusha"
        Output: {{ "action": "remember", "parameter": {{ "key": "name", "value": "Anusha" }}, "response": "I'll remember that your name is Anusha." }}

        User: "I like machine learning and deep learning"
        Output: {{ "action": "remember", "parameter": {{ "key": "interests", "value": "machine learning, deep learning" }}, "response": "Noted! I've saved your interest in machine learning and deep learning." }}

        User: "My favorite color is blue"
        Output: {{ "action": "remember", "parameter": {{ "key": "favorite_color", "value": "blue" }}, "response": "I'll remember that your favorite color is blue." }}

        User: "Search Google for Python learning"
        Output: {{ "action": "google_search", "parameter": {{ "query": "Python learning" }}, "response": "Searching Google for Python learning." }}

        User: "Play lofi beats on YouTube"
        Output: {{ "action": "youtube_play", "parameter": {{ "query": "lofi beats" }}, "response": "Playing lofi beats on YouTube." }}
        
        User: "Draft an email to friend@example.com about the party"
        Output: {{ "action": "email", "parameter": {{ "recipient": "friend@example.com", "topic": "party" }}, "response": "Drafting email..." }}
        """

        payload = {
            "model": self.model,
            "prompt": f"User: {text}",
            "system": system_prompt,
            "stream": False,
            "format": "json"
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract the 'response' field from Ollama's output structure
            model_output = result.get("response", "")
            
            # Parse the JSON string returned by the model
            try:
                command = json.loads(model_output)
            except json.JSONDecodeError:
                print(f"Failed to parse model output: {model_output}")
                return {
                    "action": "chat",
                    "parameter": None,
                    "response": model_output # Fallback to raw text
                }

            # Extended Logic: Handle 'email' action by drafting content
            if command.get("action") == "email":
                params = command.get("parameter", {})
                recipient = params.get("recipient")
                topic = params.get("topic")

                if recipient and topic:
                    print(f"Drafting email to {recipient} about {topic}...")
                    
                    # 2. Draft Content with Phi-3
                    search_query = f"Write a short, professional email to {recipient} about {topic}. Subject line and Body only."
                    
                    payload = {
                        "model": config.DRAFT_MODEL,
                        "prompt": search_query, 
                        "stream": False
                    }
                    
                    try:
                        res = requests.post(self.url, json=payload)
                        draft_text = res.json().get("response", "")
                        
                        return {
                            "action": "send_email",
                            "parameter": {
                                "recipient": recipient,
                                "subject": f"Summary: {topic}",
                                "body": draft_text
                            },
                            "response": f"I've drafted and sent an email to {recipient} about {topic}."
                        }
                    except Exception as e:
                        print(f"Drafting failed: {e}")
                        return {
                            "action": "chat", 
                            "parameter": None, 
                            "response": "Failed to draft email."
                        }
                else:
                     return {
                        "action": "chat",
                        "parameter": None,
                        "response": "I need a recipient and a topic to send an email."
                    }
        
            # Pass through for other actions including whatsapp_msg
            return command

        except Exception as e:
            print(f"Brain Error: {e}")
            return {
                "action": "chat",
                "parameter": None,
                "response": "I'm having trouble thinking right now."
            }

if __name__ == "__main__":
    b = Brain()
    # print(b.process("Open Notepad"))
