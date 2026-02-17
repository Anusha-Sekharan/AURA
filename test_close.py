import time
from executor import Executor

def test_app_lifecycle():
    e = Executor()
    
    print("Test 1: Opening Notepad...")
    result_open = e.execute("open_app", "notepad")
    print(f"Open Result: {result_open}")
    
    # Wait for the app to fully open
    time.sleep(3)
    
    print("Test 2: Closing Notepad...")
    result_close = e.execute("close_app", "notepad")
    print(f"Close Result: {result_close}")

if __name__ == "__main__":
    test_app_lifecycle()
