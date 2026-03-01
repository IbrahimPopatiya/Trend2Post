import re
from typing import List


class ContentCleaner:
    """
    Cleans and normalizes raw scraped content.
    """

    def __init__(self, min_line_length: int = 40):
        self.min_line_length = min_line_length

    def clean(self, raw_text: str) -> str:
        """
        Clean raw scraped text into high-quality content.
        """
        if not raw_text:
            return ""

        # Split into lines
        lines = raw_text.split("\n")

        cleaned_lines: List[str] = []

        for line in lines:
            line = line.strip()

            # Skip empty or very short lines
            if len(line) < self.min_line_length:
                continue

            # Skip common noise patterns
            if self._is_noise(line):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _is_noise(self, line: str) -> bool:
        """
        Detect noisy lines like navigation, cookies, social links.
        """
        noise_patterns = [
            r"cookie",
            r"privacy policy",
            r"terms of service",
            r"subscribe",
            r"sign up",
            r"twitter",
            r"linkedin",
            r"github",
            r"©",
        ]

        line_lower = line.lower()
        return any(re.search(pattern, line_lower) for pattern in noise_patterns)