import os
import shutil
from executor import Executor

def test_delete_folder():
    print("Testing delete_folder...")
    e = Executor()
    
    # Setup: Create dummy folders to delete
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    folder_1 = "DeleteMe_Desktop"
    full_path_1 = os.path.join(desktop_path, folder_1)
    if not os.path.exists(full_path_1):
        os.makedirs(full_path_1)
        
    folder_2 = "DeleteMe_Downloads"
    full_path_2 = os.path.join(downloads_path, folder_2)
    if not os.path.exists(full_path_2):
        os.makedirs(full_path_2)

    # Test 1: Delete folder on Desktop
    result_1 = e.execute("delete_folder", {"name": folder_1, "path": "desktop"})
    print(f"Test 1 Result: {result_1}")
    
    if not os.path.exists(full_path_1):
        print("PASS: Folder deleted from Desktop.")
    else:
        print("FAIL: Folder still exists on Desktop.")

    # Test 2: Delete folder in Downloads
    result_2 = e.execute("delete_folder", {"name": folder_2, "path": "downloads"})
    print(f"Test 2 Result: {result_2}")
    
    if not os.path.exists(full_path_2):
        print("PASS: Folder deleted from Downloads.")
    else:
        print("FAIL: Folder still exists in Downloads.")
        
    # Test 3: Delete non-existent folder
    result_3 = e.execute("delete_folder", {"name": "NonExistentFolder123", "path": "desktop"})
    print(f"Test 3 Result: {result_3}")
    if "does not exist" in result_3:
        print("PASS: Coping with non-existent folder.")
    else:
        print("FAIL: Incorrect response for non-existent folder.")

if __name__ == "__main__":
    test_delete_folder()
