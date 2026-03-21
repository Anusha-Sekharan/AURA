import pyttsx3
import config
import threading
import queue
import platform

class Speaker:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.running = True
        
        # Start the dedicated TTS thread
        self.thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.thread.start()

    def _tts_worker(self):
        # pyttsx3 on Windows requires COM initialization per thread
        if platform.system() == "Windows":
            try:
                import comtypes
                comtypes.CoInitialize()
            except ImportError:
                pass
                
        engine = pyttsx3.init()
        engine.setProperty('rate', config.TTS_RATE)
        engine.setProperty('volume', 1.0)
        
        voices = engine.getProperty('voices')
        for voice in voices:
            if "Zira" in voice.name:
                engine.setProperty('voice', voice.id)
                break
                
        while self.running:
            try:
                text = self.message_queue.get(timeout=1)
                if text is None:
                    break
                    
                print(f"AURA: {text}")
                try:
                    engine.say(text)
                    engine.runAndWait()
                except RuntimeError:
                    # Occurs if run loop already started or broken state, try to reinit
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                    
                self.message_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TTS Error: {e}")

    def speak(self, text):
        """Adds text to the queue to be spoken by the background thread."""
        self.message_queue.put(text)
        
    def stop(self):
        self.running = False
        self.message_queue.put(None)
        if self.thread.is_alive():
            self.thread.join(timeout=2)

if __name__ == "__main__":
    import time
    s = Speaker()
    s.speak("Systems online.")
    time.sleep(2)
    s.stop()
