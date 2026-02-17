from executor import Executor

def test_translation():
    print("Testing Translation Feature...")
    e = Executor()
    
    # Test 1: English to Spanish
    print("\n--- English to Spanish ---")
    res_es = e.execute("translate", {"text": "Hello world", "target": "spanish"})
    print(f"Result: {res_es}")
    if "Hola" in res_es or "mundo" in res_es:
        print("PASS: Translated to Spanish.")
    else:
        print("FAIL: Spanish translation check failed.")

    # Test 2: English to French
    print("\n--- English to French ---")
    res_fr = e.execute("translate", {"text": "Good morning", "target": "french"})
    print(f"Result: {res_fr}")
    if "Bonjour" in res_fr:
        print("PASS: Translated to French.")
    else:
        print("FAIL: French translation check failed.")

if __name__ == "__main__":
    test_translation()
