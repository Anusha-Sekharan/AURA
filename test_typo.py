from brain import Brain

def test_typo_correction():
    b = Brain()
    text = "Close whtasapp"
    print(f"Testing input: {text}")
    
    result = b.process(text)
    print("Result:", result)
    
    if result.get("action") == "close_app":
        param = result.get("parameter")
        print(f"Parameter: {param}")
        if param == "whatsapp":
            print("SUCCESS: Typo corrected.")
        else:
            print(f"WARNING: Typo not corrected, got '{param}'.")
    else:
        print("FAILURE: Intent not recognized.")

if __name__ == "__main__":
    test_typo_correction()
