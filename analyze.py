# analyze.py
def count_letters(text: str) -> int:
    """Counts only alphabetic letters in the text."""
    return sum(1 for ch in text if ch.isalpha())

