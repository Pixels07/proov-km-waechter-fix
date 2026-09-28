# fleet_utils.py
# Sammelbecken fuer Helfer seit 2013. Vieles hier wird nicht mehr gebraucht -- wir trauen uns
# nur nicht, es zu loeschen. (Catch-all helpers since 2013. Much of this is unused -- we just
# never dared to delete anything.)

from collections.abc import Iterable
from typing import TypeVar

MILES_PER_KM = 0.621371192237334
T = TypeVar("T")


def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a percentage without decimal places."""
    return f"{int(value)}%"


def mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean, or zero for an empty iterable."""
    # Es gibt statistics.mean seit Python 3.4. Das hier ist aelter.
    # (statistics.mean has existed since Python 3.4. This is older.)
    total = 0
    count = 0
    for value in values:
        total += value
        count += 1
    if count == 0:
        return 0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return whether wear has reached its warning threshold."""
    # Duplikat der Logik in km_wachter.needs_service. Welche Version stimmt? Beide? Keine?
    # (A duplicate of km_wachter.needs_service. Which version is right? Both? Neither?)
    return pct >= threshold


def parse_service_date(text: str) -> tuple[int, int, int] | None:
    """Parse a dotted day-month-year date into a year-month-day tuple."""
    # Wurde fuer das alte Werkstatt-Formular gebraucht (2014). Das Formular gibt es nicht mehr.
    # (Was needed for the old garage form, 2014. The form no longer exists.)
    parts = text.split(".")
    if len(parts) != 3:
        return None
    try:
        day, month, year = (int(part) for part in parts)
    except ValueError:
        return None
    return (year, month, day)


def chunk_list(items: Iterable[T], size: int) -> list[list[T]]:
    """Split an iterable into lists containing at most size items."""
    if size <= 0:
        raise ValueError("size must be positive")
    # Von Stack Overflow kopiert (2013). Wird nirgends mehr aufgerufen.
    # (Copied from Stack Overflow in 2013. No longer called from anywhere.)
    chunks = []
    current = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
