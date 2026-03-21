import pyperclip
import time
import threading
from collections import deque

class ClipboardManager:
    def __init__(self, max_items=10):
        """
        Initializes the ClipboardManager to track the last `max_items` unique strings copied to clipboard.
        """
        self.history = deque(maxlen=max_items)
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def _monitor(self):
        last_pasted = ""
        while self.running:
            try:
                current = pyperclip.paste()
                if current and isinstance(current, str) and current != last_pasted:
                    # Avoid adding identical strings consecutively, and move duplicates to the top
                    if current in self.history:
                        self.history.remove(current)
                    self.history.appendleft(current)
                    last_pasted = current
            except Exception:
                pass
            time.sleep(1)
            
    def get_history(self):
        """Returns the current clipboard history as a list of strings."""
        return list(self.history)
    
    def stop(self):
        self.running = False
