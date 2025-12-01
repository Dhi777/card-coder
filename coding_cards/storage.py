# coding_cards/storage.py

"""
Handles JSON storage for cards.

Responsibilities:
- Load cards from file
- Save cards to file
"""

import json
from pathlib import Path
from typing import List

from .models import BaseCard, card_to_dict, card_from_dict


class CardStorage:
    def __init__(self, storage_path: str = "data/cards.json"):
        self.storage_path = Path(storage_path)
        # Ensure the parent folder (data/) exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[BaseCard]:
        """Load cards from JSON file. Returns an empty list if file is missing."""
        if not self.storage_path.exists():
            return []

        with self.storage_path.open("r", encoding="utf-8") as f:
            raw_list = json.load(f)

        return [card_from_dict(item) for item in raw_list]

    def save(self, cards: List[BaseCard]) -> None:
        """Save card objects to JSON file."""
        serializable = [card_to_dict(c) for c in cards]
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=4, ensure_ascii=False)
