try:
    with open('log.txt', 'r', encoding='utf-16') as f:
        content = f.read()
    with open('log_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Conversion done.")
except Exception as e:
    print(f"Error: {e}")
