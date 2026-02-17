import pyttsx3
import config

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', config.TTS_RATE)
        self.engine.setProperty('volume', 1.0)
        
        # Try to set Zira (Female) voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "Zira" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break

    def speak(self, text):
        print(f"AURA: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    s = Speaker()
    s.speak("Systems online.")
