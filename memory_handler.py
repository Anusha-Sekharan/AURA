import json
import os

class MemoryHandler:
    def __init__(self, filepath="data/memory.json"):
        self.filepath = filepath
        self._ensure_data_dir()
        self.memory = self._load_memory()

    def _ensure_data_dir(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_memory(self):
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: memory.json is corrupted. Starting with empty memory.")
            return {}

    def save_memory(self, key, value):
        """Saves a specific key-value pair to memory."""
        self.memory[key] = value
        self._write_to_file()
        return f"Memory updated: {key} = {value}"

    def delete_memory(self, key):
        """Deletes a specific key from memory."""
        if key in self.memory:
            del self.memory[key]
            self._write_to_file()
            return f"Memory deleted: {key}"
        return f"Key '{key}' not found in memory."

    def _write_to_file(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def get_memory_string(self):
        """Returns a formatted string of memory for the system prompt."""
        if not self.memory:
            return ""
        
        memory_str = "User's Details / Persistent Memory:\n"
        for k, v in self.memory.items():
            memory_str += f"- {k}: {v}\n"
        return memory_str
