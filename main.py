import time
from listener import Listener
from speaker import Speaker
from brain import Brain
from executor import Executor
import config

def main():
    print("Initializing AURA...")

    ear = Listener()
    mouth = Speaker()
    brain = Brain()
    hand = Executor(mouth)
    
    mouth.speak("Aura online. Waiting for command.")
    
    while True:
        try:
            # 1. Listen / Input
            # text = ear.listen()  # Voice mode
            text = input("User: ") # Text mode

            
            if "exit" in text or "quit" in text:
                mouth.speak("Shutting down.")
                break

            # 2. Think
            command = brain.process(text)
            
            # 3. Speak Response
            response_text = command.get("response", "")
            if response_text:
                mouth.speak(response_text)
            
            # 4. Act
            action = command.get("action")
            parameter = command.get("parameter")
           
            if action and action != "chat":
                result = hand.execute(action, parameter)
                print(f"Action Result: {result}")
                if result:
                    mouth.speak(result) 

        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
