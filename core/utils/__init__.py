import re

CYRILLIC_TO_LATIN = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "ж": "zh", "з": "z", "и": "i", "й": "y",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sht", "ъ": "a",
    "ь": "", "ю": "yu", "я": "ya",
}


def cyrillic_slugify(value: str) -> str:
    value = value.lower().strip()

    result = ""
    for char in value:
        if char in CYRILLIC_TO_LATIN:
            result += CYRILLIC_TO_LATIN[char]
        elif char.isalnum():
            result += char
        elif char in (" ", "-", "_"):
            result += "-"
        # друго → игнор

    result = re.sub(r"-{2,}", "-", result)
    return result.strip("-")
