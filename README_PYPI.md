# Pepkio Doubling Time Tracker

Python client for the Pepkio Doubling Time Tracker REST API: calculate cell or microbial doubling time and growth rate from counts, OD600, or confluency (2-point or multi-point regression).

## Quick Start

```python
from pepkio_doubling_time_tracker import PepkioClient

with PepkioClient(api_key="your-api-key") as client:
    inp = client.get_example_input("ecoli_od600_two_point")
    result = client.run(inp)
    print(result.result)
```
