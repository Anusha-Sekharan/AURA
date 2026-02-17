from pycaw.utils import AudioUtilities
import sys

def debug_4():
    try:
        help(AudioUtilities)
    except Exception as e:
        print(e)
        
    print("-" * 20)
    dev = AudioUtilities.GetSpeakers()
    try:
        help(dev)
    except:
        pass

if __name__ == "__main__":
    sys.stdout = open('log_help.txt', 'w', encoding='utf-8')
    debug_4()
