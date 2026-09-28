"""Tests for history-based breakdown risk scoring."""

import pytest

from analyze import breakdown_averages, is_high_risk, load_history, risk_score


def test_risk_score_combines_the_three_selected_metrics() -> None:
    """A fully elevated vehicle reaches the top of the bounded score."""
    vehicle = {
        "km_since_service": 15000,
        "avg_daily_km": 250,
        "load_factor": 1.0,
    }

    assert risk_score(vehicle) == pytest.approx(100)


def test_high_risk_vehicle_is_caught_and_low_risk_vehicle_is_not() -> None:
    """The screening threshold separates high- and low-use profiles."""
    risky_vehicle = {
        "km_since_service": 14000,
        "avg_daily_km": 200,
        "load_factor": 0.8,
    }
    low_risk_vehicle = {
        "km_since_service": 4000,
        "avg_daily_km": 100,
        "load_factor": 0.4,
    }

    assert risk_score(risky_vehicle) > risk_score(low_risk_vehicle)
    assert is_high_risk(risky_vehicle)
    assert not is_high_risk(low_risk_vehicle)


def test_history_comparison_uses_only_the_selected_metrics() -> None:
    """Historical averages reflect the three requested columns only."""
    rows = [
        {
            "broke_down": "0",
            "km_since_service": "6000",
            "avg_daily_km": "100",
            "load_factor": "0.4",
            "odometer_km": "100000",
            "age_years": "10",
        },
        {
            "broke_down": "1",
            "km_since_service": "12000",
            "avg_daily_km": "160",
            "load_factor": "0.6",
            "odometer_km": "1000",
            "age_years": "1",
        },
    ]

    averages = breakdown_averages(rows)

    assert averages[0] == {
        "km_since_service": 6000,
        "avg_daily_km": 100,
        "load_factor": 0.4,
    }
    assert averages[1] == {
        "km_since_service": 12000,
        "avg_daily_km": 160,
        "load_factor": 0.6,
    }


def test_history_shows_higher_selected_metrics_for_breakdowns() -> None:
    """All three selected metric averages are higher for breakdown vehicles."""
    averages = breakdown_averages(load_history())

    for metric in ("km_since_service", "avg_daily_km", "load_factor"):
        assert averages[1][metric] > averages[0][metric]
