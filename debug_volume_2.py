from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import comtypes

def debug_pycaw():
    print("Initializing COM...")
    try:
        comtypes.CoInitialize()
    except:
        pass

    devices = AudioUtilities.GetSpeakers()
    print(f"Device: {devices}")
    print(f"Type: {type(devices)}")
    
    print("Attributes:")
    for d in dir(devices):
        if "act" in d.lower():
            print(f" - {d}")

    # Try lowercase
    try:
        interface = devices.activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        print("LOWERCASE activate worked!")
    except Exception as e:
        print(f"LOWERCASE activate failed: {e}")

    # Try uppercase
    try:
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        print("UPPERCASE Activate worked!")
    except Exception as e:
        print(f"UPPERCASE Activate failed: {e}")

if __name__ == "__main__":
    debug_pycaw()
