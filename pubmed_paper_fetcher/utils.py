import re

def extract_email(text: str) -> str:
    """Extract first email address found in a string."""
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""
