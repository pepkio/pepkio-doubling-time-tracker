# Pepkio Doubling Time Tracker

Python client for the Pepkio Doubling Time Tracker REST API: calculate cell or microbial doubling time and growth rate from counts, OD600, or confluency (2-point or multi-point regression).

## Installation

```bash
pip install pepkio-doubling-time-tracker
```

## Quick Start

```python
from pepkio_doubling_time_tracker import PepkioClient

with PepkioClient(api_key="your-api-key") as client:
    manifest = client.get_manifest()
    print(manifest["title"])

    inp = client.get_example_input("ecoli_od600_two_point")
    result = client.run(inp)
    print(result.status, result.result)
```

## CLI Usage

```bash
pepkio-doubling-time-tracker manifest
pepkio-doubling-time-tracker run --example ecoli_od600_two_point
```
