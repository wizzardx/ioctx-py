# ioctx-py

[![PyPI version](https://img.shields.io/pypi/v/ioctx.svg)](https://pypi.org/project/ioctx/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ioctx.svg)](https://pypi.org/project/ioctx/)
[![License](https://img.shields.io/github/license/wizzardx/ioctx-py.svg)](https://github.com/wizzardx/ioctx-py/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/workflow/status/wizzardx/ioctx-py/CI)](https://github.com/wizzardx/ioctx-py/actions)

A structured effects system for testable side effects in Python.

## What is ioctx?

ioctx provides a composable, reifiable approach to handling IO operations in Python. Rather than relying on ad-hoc mocking and monkeypatching, ioctx gives you a structured way to make side effects explicit, testable, and traceable.

### The Problem

Traditional approaches to testing IO in Python suffer from several limitations:

- **Global state modification**: Monkeypatching changes global state, creating test isolation problems
- **Opacity**: No structured record of which operations were intercepted or how they were handled
- **Incompleteness**: Mocking individual functions is piecemeal and requires careful tracking
- **Inflexible boundaries**: The boundary between "real" and "fake" operations is often all-or-nothing

### The Solution

ioctx provides a unified approach through the `IOContext` protocol:

- **Explicit**: IO operations are performed through a context object passed to functions
- **Composable**: Different IO contexts can be layered and combined
- **Reifiable**: All operations can be represented as data for inspection and analysis
- **Flexible**: Switch between real and simulated IO without changing function logic

## Installation

```bash
pip install ioctx
```

## Basic Usage

### Defining Functions with IO Context

```python
from ioctx import IOContext

def fetch_and_process(data_url: str, output_path: str, ctx: IOContext) -> Summary:
    """Fetch data from URL, process it, and save results."""
    # Fetch data
    response = ctx.http_get(data_url)
    if response.status_code != 200:
        ctx.log("error", f"Failed to fetch data: {response.status_code}")
        raise DataFetchError(f"HTTP error: {response.status_code}")

    # Process data
    data = parse_data(response.text)
    results = analyze_data(data)

    # Save results
    ctx.write_file(output_path, results.to_json().encode('utf-8'))
    ctx.log("info", f"Wrote results to {output_path}")

    return results.summary
```

### Using with Real IO

```python
from ioctx import RealIO

# Use real IO operations
real_ctx = RealIO()
summary = fetch_and_process(
    "https://data.example.com/dataset.json",
    "/tmp/results.json",
    real_ctx
)
```

### Testing with Fake IO

```python
from ioctx import FakeIO, HttpResponse

# Set up fake responses for testing
fake_ctx = FakeIO(
    file_contents={},
    http_responses={
        "https://data.example.com/dataset.json": HttpResponse(
            200,
            '{"records": [{"id": 1, "value": 42}, {"id": 2, "value": 17}]}'
        )
    }
)

# Test with fake IO
test_summary = fetch_and_process(
    "https://data.example.com/dataset.json",
    "/tmp/results.json",
    fake_ctx
)

assert test_summary.record_count == 2
assert test_summary.total_value == 59
```

### Logging and Tracing

```python
from ioctx import TracingIO, RealIO

# Add tracing to real operations
tracing_ctx = TracingIO(RealIO())
fetch_and_process(
    "https://data.example.com/dataset.json",
    "/tmp/results.json",
    tracing_ctx
)

# Examine trace
for operation, args, result in tracing_ctx.trace:
    print(f"Operation: {operation}")
    print(f"Arguments: {args}")
    print("Result: ", result)
    print("---")
```

## Advanced Features

### Composing IO Contexts

```python
# Create a stack of IO contexts
base_ctx = RealIO()
validated_ctx = ValidatingIO(
    base_ctx,
    allowed_domains=["api.example.com"],
    allowed_paths=["/tmp/", "/var/data/"]
)
traced_ctx = TracingIO(validated_ctx)

# Use the composed stack
result = process_data("input.csv", traced_ctx)

# Operations pass through each layer
# 1. Tracing records the call
# 2. Validation checks permissions
# 3. RealIO performs the actual IO
```

### Recording and Replaying IO

```python
# Record a sequence of operations
record_ctx = RecordingIO(RealIO())
results = complex_analysis("data/large_dataset.csv", record_ctx)
recording = record_ctx.get_recording()

# Save for later
import pickle
with open("analysis_recording.pkl", "wb") as f:
    pickle.dump(recording, f)

# Later, replay the same operations
with open("analysis_recording.pkl", "rb") as f:
    recording = pickle.load(f)

replay_ctx = ReplayIO(recording)
results2 = complex_analysis("data/large_dataset.csv", replay_ctx)
# results and results2 will be identical
```

## Why Use ioctx?

- **Testing**: Write deterministic tests for code with IO dependencies without complex mocking
- **Reproducibility**: Capture and replay exact sequences of IO operations
- **Tracing**: Record all IO for debugging, auditing, or performance analysis
- **Validation**: Enforce constraints on what IO operations are allowed
- **Simulation**: Create realistic test environments with controlled responses

## How Does ioctx Compare?

| Approach | Global State | Visibility | Composition | Reification |
|----------|--------------|------------|-------------|-------------|
| unittest.mock | Modifies | Limited | Difficult | None |
| pytest-mock | Modifies | Limited | Difficult | None |
| Manual dependency injection | Clean | Manual | Yes | Manual |
| ioctx | Clean | Built-in | Built-in | Built-in |

## Project Status

ioctx is in active development. Current roadmap:

- **Q3 2025**: Initial PyPI release with core functionality
- **Q4 2025**: Support for additional IO categories and ecosystem integration
- **Q1 2026**: Advanced tooling for analysis and visualization of IO traces

## Contributing

Contributions are welcome! The project is looking for help with:

1. Core API refinement
2. Backend implementations
3. Integration bridges
4. Documentation and examples
5. Performance optimization

Check the [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
