"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "doubling-time-tracker",
        "title": "Doubling Time Tracker",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "ecoli_od600_two_point",
                "input": {
                    "mode": "two_point",
                    "metric": "od600",
                    "time_unit": "min",
                    "sample_label": "E. coli",
                    "two_point": {
                        "t0": 0,
                        "n0": 0.1,
                        "t1": 120,
                        "n1": 0.8,
                    },
                },
                "output": {
                    "has_blocking_errors": False,
                    "fit": {
                        "doubling_time_h": 0.667,
                    },
                },
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "mode": "two_point",
            "metric": "od600",
            "fit": {
                "doubling_time_h": 0.6667,
                "growth_rate_per_h": 1.0397,
            },
            "points": [
                {"t": 0, "value": 0.1},
                {"t": 120, "value": 0.8},
            ],
            "warnings": [],
            "has_blocking_errors": False,
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
