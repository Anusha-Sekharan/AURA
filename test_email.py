import config
from brain import Brain

# Mock the Brain process but with real Ollama calls if possible
# or just test the intent parsing if I could mock the response.
# For now, I'll run a real test assuming Ollama is up.
def test_email_intent():
    b = Brain()
    
    # We can't easily mock the email drafting unless we have phi3:latest.
    # We will assume the user has it.
    
    text = "Draft a mail to test@example.com regarding the project deadline"
    print(f"Testing input: {text}")
    
    result = b.process(text)
    print("Result:", result)
    
    if result.get("action") == "send_email":
        print("SUCCESS: Identified email intent and drafted content.")
        params = result.get("parameter", {})
        print(f"Recipient: {params.get('recipient')}")
        print(f"Subject: {params.get('subject')}")
        print(f"Body Preview: {params.get('body')[:50]}...")
    else:
        print("FAILURE: Did not identify email intent.")

if __name__ == "__main__":
    test_email_intent()
