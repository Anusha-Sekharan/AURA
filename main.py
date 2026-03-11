import subprocess
import time
import sys
import os

def main():
    print("Initializing AURA via Electron...")

    # Start the Flask Backend API
    print("Starting Internal Python Backend (Flask)...")
    api_process = subprocess.Popen([sys.executable, "api.py"])
    
    # Give the backend a moment to boot
    time.sleep(2)
    
    # Start the Electron UI
    print("Starting Electron UI...")
    electron_dir = os.path.join(os.path.dirname(__file__), "ui-electron")
    ui_process = subprocess.Popen(["npx", "electron", "."], cwd=electron_dir, shell=True)
    
    try:
        # Wait for either process to terminate
        ui_process.wait()
    except KeyboardInterrupt:
        print("\nStopping AURA...")
    finally:
        # Clean up both processes when closed
        api_process.terminate()
        ui_process.terminate()
        print("AURA shutdown complete.")

if __name__ == "__main__":
    main()
