"""Breakdown cars average 11,678 km since service vs. 7,261 for others.
They also average 159.7 daily km and 0.60 load factor, vs. 131.4 and 0.51.
"""

import csv
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

HISTORY_FILE = Path(__file__).with_name("fleet_history.csv")
RISK_ALERT_SCORE = 60.0
KM_WEIGHT = 0.50
DAILY_KM_WEIGHT = 0.30
LOAD_WEIGHT = 0.20

Vehicle = Mapping[str, Any]


def risk_score(vehicle: Vehicle) -> float:
    """Return a 0-100 score from service distance, daily use, and load only."""
    km_since_service = min(max(float(vehicle["km_since_service"]) / 15000, 0), 1)
    avg_daily_km = min(max(float(vehicle["avg_daily_km"]) / 250, 0), 1)
    load_factor = min(max(float(vehicle["load_factor"]), 0), 1)
    return 100 * (
        KM_WEIGHT * km_since_service
        + DAILY_KM_WEIGHT * avg_daily_km
        + LOAD_WEIGHT * load_factor
    )


def is_high_risk(vehicle: Vehicle) -> bool:
    """Return whether a vehicle reaches the historical risk screening score."""
    return risk_score(vehicle) >= RISK_ALERT_SCORE


def load_history(path: str | Path = HISTORY_FILE) -> list[dict[str, str]]:
    """Load the labelled fleet history from a CSV file."""
    with Path(path).open(newline="") as history_file:
        return list(csv.DictReader(history_file))


def breakdown_averages(rows: Sequence[Vehicle]) -> dict[int, dict[str, float]]:
    """Calculate requested metric means for each breakdown label."""
    metrics = ("km_since_service", "avg_daily_km", "load_factor")
    result = {}
    for label in (0, 1):
        group = [row for row in rows if int(row["broke_down"]) == label]
        result[label] = {
            metric: sum(float(row[metric]) for row in group) / len(group)
            for metric in metrics
        }
    return result


def main() -> None:
    """Print historical metric averages and all vehicles ranked by risk."""
    rows = load_history()
    for label, averages in breakdown_averages(rows).items():
        outcome = "broke down" if label else "did not break down"
        print(
            f"{outcome}: km_since_service={averages['km_since_service']:.1f}, "
            f"avg_daily_km={averages['avg_daily_km']:.1f}, "
            f"load_factor={averages['load_factor']:.2f}"
        )

    ranked = sorted(rows, key=risk_score, reverse=True)
    print("\nVehicle risk scores (highest first):")
    for vehicle in ranked:
        print(f"{vehicle['car_id']}: {risk_score(vehicle):.1f}")


if __name__ == "__main__":
    main()
