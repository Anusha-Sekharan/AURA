from executor import Executor
import time

def test_web_info():
    print("Testing Web & Info Features...")
    e = Executor()
    
    # 1. Test Weather (Real Network Call)
    print("\n--- Testing Weather ---")
    res_weather = e.execute("weather", {"location": "London"})
    print(f"London Weather: {res_weather}")
    if "Weather Report" in res_weather:
        print("PASS: Weather fetched.")
    else:
        print("FAIL: Weather fetch failed.")

    # 2. Test Definition (Real Network Call)
    print("\n--- Testing Definition ---")
    res_wiki = e.execute("definition", {"term": "Python (programming language)"})
    print(f"Definition: {res_wiki}")
    if "Python" in res_wiki and ":" in res_wiki:
        print("PASS: Definition fetched.")
    else:
        print("FAIL: Definition fetch failed.")

    # 3. Test Google Search (Mocked/Browser Open)
    print("\n--- Testing Google Search ---")
    # This will open a browser tab.
    res_search = e.execute("google_search", {"query": "Test Search"})
    print(f"Search Result: {res_search}")
    if "Opened Google search" in res_search:
        print("PASS: Google search initiated.")
    else:
        print("FAIL: Google search failed.")

    # 4. Test YouTube (Mocked/Browser Open)
    print("\n--- Testing YouTube ---")
    # This will open a browser tab.
    res_yt = e.execute("youtube_play", {"query": "Test Video"})
    print(f"YouTube Result: {res_yt}")
    if "Opened YouTube" in res_yt:
        print("PASS: YouTube search initiated.")
    else:
        print("FAIL: YouTube search failed.")

if __name__ == "__main__":
    test_web_info()
