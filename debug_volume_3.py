try:
    from pycaw.utils import AudioUtilities
    print("Imported from pycaw.utils")
except ImportError:
    from pycaw.pycaw import AudioUtilities
    print("Imported from pycaw.pycaw")

from comtypes import CLSCTX_ALL
from pycaw.pycaw import IAudioEndpointVolume

def debug_3():
    devices = AudioUtilities.GetSpeakers()
    print(f"Device: {devices}")
    
    # Check _device
    try:
        real_dev = devices._device
        print(f"Real Device: {real_dev}")
        print(f"Real Device Activate? {hasattr(real_dev, 'Activate')}")
        
        # Try activating real device
        interface = real_dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        print("Activation via _device success!")
    except Exception as e:
        print(f"Accessing _device failed: {e}")

if __name__ == "__main__":
    debug_3()
