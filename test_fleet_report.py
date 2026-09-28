# test_fleet_report.py
import pytest

from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars() -> None:
    """The summary counts cars at or above the wear threshold."""
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_handles_missing_last_service_reading() -> None:
    """A missing service reading does not crash or distort known wear."""
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},
    ]
    summary = fleet_summary(fleet)

    assert summary["count"] == 2
    assert summary["average_wear"] == pytest.approx(99.33333333333333)
