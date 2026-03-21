from executor import Executor
import sys

class MockSpeaker:
    def speak(self, text):
        print(f"Speak: {text}")

e = Executor(MockSpeaker())
try:
    print("Trying to close chrome...")
    res = e.execute("close_app", "chrome")
    print(f"Result: {res}")
except Exception as ex:
    print(f"Exception: {ex}")

try:
    print("Trying to close github...")
    res = e.execute("close_app", "github")
    print(f"Result: {res}")
except Exception as ex:
    print(f"Exception: {ex}")
