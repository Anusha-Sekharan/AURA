import pyttsx3

try:
    print("Initializing engine...")
    engine = pyttsx3.init()
    
    print("Listing voices:")
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f" - {voice.name} ({voice.id})")
        
    print("\nTesting default voice...")
    engine.say("This is a test of the Aura voice system.")
    engine.runAndWait()
    print("Test complete.")
    
except Exception as e:
    print(f"Voice Error: {e}")
