"""
Models for cards used in the Coding Cards application.

Phase 1:
- BaseCard: shared properties
- QACard: question/answer cards
- CodingCard: coding practice cards
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
import datetime

class BaseCard:
    """Base class for all card types."""
    id: str
    title: str
    concept: str
    categories: List[str]
    difficulty: str       # "easy", "medium", "hard"
    important: bool       # user-marked priority
    card_type: str        # "qa" or "coding"

    # spaced repetition fields – simple defaults for now
    next_review_date: datetime.date = field(
        default_factory=datetime.date.today
    )
    success_rate: float = 0.0
    times_seen: int = 0
    times_correct: int = 0

class QACard(BaseCard):
    """Question/Answer card model."""
    question: str
    answer: str
    
class CodingCard(BaseCard):
    """Coding practice card model."""
    starter_code: str
    solution_code: str
    test_cases: List[Dict[str, Any]]  # e.g. {"input": [...], "expected": ...}

def card_to_dict(card: BaseCard) -> Dict[str, Any]:
    """
    Convert a card dataclass to a JSON-serializable dict.
    Handles non-JSON types like datetime.date.
    """
    data=asdict(card)
    data["next_review_date"] = data["next_review_date"].isoformat()
    return data

def card_from_dict(data: Dict[str, Any]) -> BaseCard:
    """
    Convert a dict (loaded from JSON) back into the correct card type.
    """
    # convert next_review_date back to date object
    if isinstance(data.get("next_review_date"), str):
        data["next_review_date"] = datetime.date.fromisoformat(
            data["next_review_date"]
        )

    card_type = data.get("card_type")
    if card_type == "qa":
        return QACard(**data)
    elif card_type == "coding":
        return CodingCard(**data)
    else:
        raise ValueError(f"Unknown card_type: {card_type}")
