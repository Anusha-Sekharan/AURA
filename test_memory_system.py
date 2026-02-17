import os
import shutil
from memory_handler import MemoryHandler
from executor import Executor

def test_memory_handler():
    print("Testing MemoryHandler...")
    # Setup clean state
    test_file = "data/test_memory.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    mh = MemoryHandler(filepath=test_file)
    
    # Test Save
    mh.save_memory("name", "Test User")
    mh.save_memory("color", "Blue")
    
    # Test Load (re-instantiate)
    mh2 = MemoryHandler(filepath=test_file)
    memory = mh2._load_memory()
    
    assert memory.get("name") == "Test User"
    assert memory.get("color") == "Blue"
    print("MemoryHandler Save/Load: PASS")
    
    # Test String Format
    s = mh2.get_memory_string()
    assert "Test User" in s
    assert "Blue" in s
    print("MemoryHandler String Format: PASS")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

def test_executor_remember():
    print("\nTesting Executor Remember...")
    # We will use the default memory file for this, so we might effect real memory.
    # Let's mock the memory handler inside executor for safety or just use a temp one by patching?
    # Since we can't easily patch without unittest.mock, let's just back up the real file.
    
    real_file = "data/memory.json"
    backup_file = "data/memory_backup.json"
    
    if os.path.exists(real_file):
        shutil.copy(real_file, backup_file)
        
    try:
        ex = Executor()
        # Point to a test file dynamically if possible, but Executor inits MemoryHandler() directly.
        # We can manually swap it.
        test_mh = MemoryHandler(filepath="data/test_executor_memory.json")
        ex.memory = test_mh
        
        result = ex.execute("remember", {"key": "test_key", "value": "test_value"})
        print(f"Result: {result}")
        
        saved_val = test_mh.memory.get("test_key")
        assert saved_val == "test_value"
        print("Executor Remember: PASS")
        
        # Cleanup test file
        if os.path.exists("data/test_executor_memory.json"):
            os.remove("data/test_executor_memory.json")
            
    finally:
        # Restore real memory if validation fails or finishes
        if os.path.exists(backup_file):
            shutil.move(backup_file, real_file)

if __name__ == "__main__":
    try:
        test_memory_handler()
        test_executor_remember()
        print("\nAll Tests Passed!")
    except Exception as e:
        print(f"\nTests Failed: {e}")
