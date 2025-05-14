"""
Tests for ioctx using the dogfooding approach.

This module demonstrates the dogfooding approach to testing the ioctx library,
where we use the library itself to create testable environments.
"""

import os
import tempfile

import pytest

from ioctx import FakeIO, HttpResponse, IOContext, RealIO, TracingIO


# A simple function that uses IOContext for its operations
def fetch_and_save(url: str, output_path: str, ctx: IOContext) -> int:
    """Fetch data from a URL and save it to a file.

    Args:
        url: The URL to fetch data from.
        output_path: The path to save the data to.
        ctx: The IOContext to use for IO operations.

    Returns:
        The HTTP status code.
    """
    # Fetch the data
    response = ctx.http_get(url)

    # Log the status
    ctx.log("info", f"Received status code {response.status_code} from {url}")

    # Save the data if successful
    if response.status_code == 200:
        ctx.write_file(output_path, response.text.encode("utf-8"))
        ctx.log("info", f"Wrote {len(response.text)} bytes to {output_path}")
    else:
        ctx.log("error", f"Failed to fetch data: {response.status_code}")

    return response.status_code


# Test using FakeIO - this demonstrates using ioctx to test a function that uses ioctx
def test_fetch_and_save_success():
    """Test fetch_and_save with a successful HTTP response."""
    # Create a fake IO context with predetermined responses
    fake_ctx = FakeIO(
        http_responses={
            "https://example.com/data": HttpResponse(
                status_code=200,
                text="Example data",
            )
        }
    )

    # Call the function with our fake context
    status_code = fetch_and_save("https://example.com/data", "/tmp/output.txt", fake_ctx)

    # Assertions
    assert status_code == 200
    assert "/tmp/output.txt" in fake_ctx.written_files
    assert fake_ctx.written_files["/tmp/output.txt"] == b"Example data"

    # Check logs
    assert any("Received status code 200" in msg for _, msg in fake_ctx.logs)
    assert any("Wrote 12 bytes" in msg for _, msg in fake_ctx.logs)


def test_fetch_and_save_error():
    """Test fetch_and_save with a failed HTTP response."""
    # Create a fake IO context with predetermined error response
    fake_ctx = FakeIO(
        http_responses={
            "https://example.com/data": HttpResponse(
                status_code=404,
                text="Not Found",
            )
        }
    )

    # Call the function with our fake context
    status_code = fetch_and_save("https://example.com/data", "/tmp/output.txt", fake_ctx)

    # Assertions
    assert status_code == 404
    assert "/tmp/output.txt" not in fake_ctx.written_files

    # Check logs
    assert any("Received status code 404" in msg for _, msg in fake_ctx.logs)
    assert any("Failed to fetch data: 404" in msg for _, msg in fake_ctx.logs)


# Test using TracingIO - dogfooding approach where we test the TracingIO implementation
def test_tracing_io():
    """Test that TracingIO properly records operations."""
    # Create a fake IO to serve as the base
    fake_ctx = FakeIO(file_contents={"/tmp/test.txt": b"test data"})

    # Create a tracing IO that wraps the fake IO
    tracing_ctx = TracingIO(fake_ctx)

    # Perform some operations
    tracing_ctx.read_file("/tmp/test.txt")
    tracing_ctx.write_file("/tmp/output.txt", b"output data")
    tracing_ctx.log("info", "Test log message")

    # Check the trace
    trace = tracing_ctx.get_trace()

    assert len(trace) == 3
    assert trace[0][0] == "read_file"
    assert trace[0][1]["path"] == "/tmp/test.txt"
    assert trace[0][2] == b"test data"

    assert trace[1][0] == "write_file"
    assert trace[1][1]["path"] == "/tmp/output.txt"
    assert trace[1][1]["content_size"] == len(b"output data")

    assert trace[2][0] == "log"
    assert trace[2][1]["level"] == "info"
    assert trace[2][1]["message"] == "Test log message"


# Integration test that uses RealIO - but only if explicitly enabled
@pytest.mark.skipif(
    not os.environ.get("IOCTX_RUN_REAL_TESTS"),
    reason="Skipping tests with real IO operations. Set IOCTX_RUN_REAL_TESTS=1 to enable.",
)
def test_real_io_integration():
    """Integration test with real IO operations."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Create a tracing context that wraps RealIO for recording
        tracing_ctx = TracingIO(RealIO())

        # Call the function with our tracing context
        status_code = fetch_and_save("https://httpbin.org/get", tmp_path, tracing_ctx)

        # Assertions - note that these are real IO operations!
        assert status_code == 200

        # Verify the file was written
        with open(tmp_path, "rb") as f:
            content = f.read()
            assert b'"url": "https://httpbin.org/get"' in content

        # Check the trace
        trace = tracing_ctx.get_trace()
        assert any(op == "http_get" for op, _, _ in trace)
        assert any(op == "write_file" for op, _, _ in trace)
        assert any(op == "log" for op, _, _ in trace)

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)  # Fixed the indentation error here
