"""Small helpers for explicit, affirmative consent recording."""


def parse_consent(value: str | None) -> int:
    """Return 1 only for an explicit affirmative answer; blank input is not consent."""
    return int((value or "").strip().casefold() in {"s", "si", "sí", "y", "yes"})
