import os
import shutil
from executor import Executor

def test_create_folder():
    print("Testing create_folder...")
    e = Executor()
    
    # Test 1: Create folder on Desktop (Default)
    folder_name = "TestFolderFromAura"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    full_path_1 = os.path.join(desktop_path, folder_name)
    
    # Cleanup before test
    if os.path.exists(full_path_1):
        os.rmdir(full_path_1)

    result = e.execute("create_folder", {"name": folder_name, "path": "desktop"})
    print(f"Test 1 Result: {result}")
    
    if os.path.exists(full_path_1):
        print("PASS: Folder created on Desktop.")
        # Cleanup
        os.rmdir(full_path_1)
    else:
        print("FAIL: Folder not found on Desktop.")

    # Test 2: Create folder in Downloads
    folder_name_2 = "AuraDownloadsTest"
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    full_path_2 = os.path.join(downloads_path, folder_name_2)
    
    # Cleanup before test
    if os.path.exists(full_path_2):
        os.rmdir(full_path_2)

    result = e.execute("create_folder", {"name": folder_name_2, "path": "downloads"})
    print(f"Test 2 Result: {result}")
    
    if os.path.exists(full_path_2):
        print("PASS: Folder created in Downloads.")
        # Cleanup
        os.rmdir(full_path_2)
    else:
        print("FAIL: Folder not found in Downloads.")

if __name__ == "__main__":
    test_create_folder()
