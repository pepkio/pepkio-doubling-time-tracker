"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_doubling_time_tracker.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY") or os.getenv("PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "doubling-time-tracker"
    names = live_client.list_examples()
    assert "ecoli_od600_two_point" in names


def test_run_ecoli_example(live_client: PepkioClient):
    inp = live_client.get_example_input("ecoli_od600_two_point")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert "fit" in result.result
    assert result.result.get("error") is None


def test_run_hela_example(live_client: PepkioClient):
    inp = live_client.get_example_input("hela_cell_count")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert "fit" in result.result


def test_run_yeast_example(live_client: PepkioClient):
    inp = live_client.get_example_input("yeast_time_series")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert "fit" in result.result
