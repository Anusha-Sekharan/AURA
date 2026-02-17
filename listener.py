import speech_recognition as sr
import config

class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"User: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                print("Network error.")
                return None

if __name__ == "__main__":
    l = Listener()
    l.listen()
