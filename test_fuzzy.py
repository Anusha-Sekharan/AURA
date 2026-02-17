from executor import Executor

def test_fuzzy_close():
    e = Executor()
    print("Testing 'close_app' with typo 'whtasapp'...")
    
    # This won't actually close WhatsApp if it's not running, but we should see the log output
    # identifying the fuzzy match.
    result = e.close_application("whtasapp")
    print(f"Result: {result}")

if __name__ == "__main__":
    test_fuzzy_close()
