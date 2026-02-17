from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import comtypes

def debug_pycaw():
    print("Initializing COM...")
    try:
        comtypes.CoInitialize()
    except Exception as e:
        print(f"CoInitialize warning: {e}")

    print("Getting Speakers...")
    devices = AudioUtilities.GetSpeakers()
    print(f"Devices Type: {type(devices)}")
    print(f"Devices Dir: {dir(devices)}")
    
    try:
        print("Attempting to Activate...")
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        print("Activate successful.")
    except Exception as e:
        print(f"Activate failed: {e}")

    # Alternative: Get all devices
    print("\nListing all devices:")
    try:
        all_devices = AudioUtilities.GetAllDevices()
        for dev in all_devices:
            print(f"- {dev}")
    except Exception as e:
        print(f"GetAllDevices failed: {e}")

if __name__ == "__main__":
    debug_pycaw()
