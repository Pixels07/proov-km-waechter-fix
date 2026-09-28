# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Nobody has cleaned it up since.

from collections.abc import Iterable, Mapping
from typing import Any

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


Car = Mapping[str, Any]


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return service-interval wear as a percentage."""
    return km_since_service / interval * 100


def needs_service(car: Car) -> bool:
    """Check whether a car with a service reading has reached the warning threshold."""
    last = car.get("last_service_km")
    if last is None:
        return False
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: Iterable[Car]) -> list[str]:
    """Print and return the IDs of cars that need service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
