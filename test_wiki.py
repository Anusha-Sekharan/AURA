from executor import Executor

def test_wiki():
    print("Testing Wikipedia...")
    e = Executor()
    
    # Test Definition
    res_wiki = e.execute("definition", {"term": "Python (programming language)"})
    print(f"Definition: {res_wiki}")
    if "Python" in res_wiki:
        print("PASS: Definition fetched.")
    else:
         print("FAIL: Definition fetch failed.")

if __name__ == "__main__":
    test_wiki()
