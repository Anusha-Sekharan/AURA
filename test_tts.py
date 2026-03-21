import threading
import time
from speaker import Speaker

def test_concurrency():
    s = Speaker()
    
    def worker(idx):
        print(f"Thread {idx} requesting speech")
        s.speak(f"Test message from thread {idx}")

    threads = []
    # Spawn 5 concurrent threads asking to speak exactly at the same time
    for i in range(5):
        t = threading.Thread(target=worker, args=(i, ))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("All threads finished requesting.")
    # Wait for speaker to actually finish speaking
    time.sleep(10)
    s.stop()
    print("Test complete.")

if __name__ == "__main__":
    test_concurrency()
