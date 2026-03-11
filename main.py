import time
from listener import Listener
from speaker import Speaker
from brain import Brain
from executor import Executor
import config
from ui import AuraUI

def main():
    print("Initializing AURA UI...")

    ear = Listener()
    mouth = Speaker()
    brain = Brain()
    hand = Executor(mouth)
    
    # Initialize and run the UI
    app = AuraUI(brain=brain, executor=hand, speaker=mouth)
    app.run()

if __name__ == "__main__":
    main()
