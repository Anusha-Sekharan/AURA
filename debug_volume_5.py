from pycaw.utils import AudioUtilities

def debug_5():
    try:
        devices = AudioUtilities.GetSpeakers()
        print(f"Device: {devices}")
        
        # Try EndpointVolume property
        print("Accessing EndpointVolume...")
        volume = devices.EndpointVolume
        print(f"Volume Interface: {volume}")
        
        # check if it has SetMute
        print(f"Has SetMute: {hasattr(volume, 'SetMute')}")
        print(f"Has SetMasterVolumeLevelScalar: {hasattr(volume, 'SetMasterVolumeLevelScalar')}")
        
        # Try getting volume
        current = volume.GetMasterVolumeLevelScalar()
        print(f"Current Volume: {current}")
        
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    debug_5()
