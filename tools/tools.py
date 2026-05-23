
from core.state import STATE

def word_counter():
    text = STATE["current_text"]
    words = text.split()
    return len(words)

def common_word_finder(text: str):
    words = text.lower().split()
    most_common = max(set(words), key=words.count)
    count = words.count(most_common)
    return f"{most_common} ({count} times)"6
STATE["current_text"]