import os
from executor import Executor
import time

def test_system_control():
    print("Testing System Control Features...")
    e = Executor()
    
    # 1. Test Screenshot
    print("\n--- Testing Screenshot ---")
    result = e.execute("screenshot", None)
    print(f"Result: {result}")
    if "Screenshot saved" in result:
        print("PASS: Screenshot taken.")
    else:
        print("FAIL: Screenshot failed.")

    # 2. Test Volume Control
    print("\n--- Testing Volume Control ---")
    
    # Mute
    res_mute = e.execute("volume_control", {"action": "mute"})
    print(f"Mute: {res_mute}")
    time.sleep(1)
    
    # Unmute
    res_unmute = e.execute("volume_control", {"action": "unmute"})
    print(f"Unmute: {res_unmute}")
    time.sleep(1)
    
    # Set Volume (Low to be safe)
    res_set = e.execute("volume_control", {"action": "set", "value": "15"})
    print(f"Set 15%: {res_set}")
    
    # Set Invalid
    res_inv = e.execute("volume_control", {"action": "set", "value": "200"})
    print(f"Set 200%: {res_inv}")

    # 3. Test Power Control (Mocked - we won't actually shut down)
    print("\n--- Testing Power Control (Safe Mode) ---")
    # We are calling the method but since "executor" uses os.system directly, 
    # we should check if it returns the correct initiation message.
    # WARNING: This MIGHT actually shut down if I'm not careful. 
    # The executor code says: "Shutting down the system in 10 seconds."
    # Command: "shutdown /s /t 10"
    # To be safe, let's NOT run the actual power commands in this test.
    # We will verify the logic by passing a dummy action if possible, 
    # or just trust the code since it is standard os.system calls.
    
    # Instead, let's verify invalid action response
    res_pow = e.execute("power_control", {"action": "dance"})
    print(f"Invalid Power Action: {res_pow}")
    if "Unknown power action" in res_pow:
        print("PASS: Handled invalid power action.")
    else:
        print("FAIL: Did not handle invalid power action.")

if __name__ == "__main__":
    test_system_control()
