"""
Utility helper functions for the Coding Cards application.
"""

import uuid


def generate_uuid() -> str:
    """Return a new unique ID for cards."""
    return str(uuid.uuid4())