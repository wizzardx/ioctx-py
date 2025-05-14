"""
ioctx - Backend implementations of the IOContext protocol.

This module provides concrete implementations of the IOContext protocol.
"""

import logging
import subprocess
from typing import Any, Dict, List, Optional, Tuple

from .protocol import CommandResult, HttpResponse, IOContext


class RealIO(IOContext):
    """Implementation that performs real IO operations.

    This class implements the IOContext protocol by using standard Python libraries
    to perform actual IO operations.
    """

    def read_file(self, path: str) -> bytes:
        """Read a file and return its contents as bytes."""
        with open(path, "rb") as f:
            return f.read()

    def write_file(self, path: str, content: bytes) -> None:
        """Write content to a file at the specified path."""
        with open(path, "wb") as f:
            f.write(content)

    def http_get(self, url: str, **kwargs: Any) -> HttpResponse:
        """Perform an HTTP GET request using the requests library."""
        try:
            import requests
        except ImportError:
            raise ImportError(
                "The 'requests' library is required for real HTTP operations. "
                "Please install it with 'pip install requests'."
            )

        response = requests.get(url, **kwargs)
        return HttpResponse(
            status_code=response.status_code, text=response.text, headers=dict(response.headers)
        )

    def http_post(self, url: str, data: Any, **kwargs: Any) -> HttpResponse:
        """Perform an HTTP POST request using the requests library."""
        try:
            import requests
        except ImportError:
            raise ImportError(
                "The 'requests' library is required for real HTTP operations. "
                "Please install it with 'pip install requests'."
            )

        response = requests.post(url, data=data, **kwargs)
        return HttpResponse(
            status_code=response.status_code, text=response.text, headers=dict(response.headers)
        )

    def execute_command(self, cmd: List[str]) -> CommandResult:
        """Execute a shell command using subprocess."""
        result = subprocess.run(cmd, capture_output=True, text=True)
        return CommandResult(
            return_code=result.returncode, stdout=result.stdout, stderr=result.stderr
        )

    def log(self, level: str, message: str) -> None:
        """Log a message using the standard logging library."""
        logging_func = getattr(logging, level.lower())
        logging_func(message)


class FakeIO(IOContext):
    """Implementation that provides predetermined responses.

    This class implements the IOContext protocol by returning predetermined
    responses without performing actual IO operations. It's useful for testing.
    """

    def __init__(
        self,
        file_contents: Optional[Dict[str, bytes]] = None,
        http_responses: Optional[Dict[str, HttpResponse]] = None,
        command_results: Optional[Dict[str, CommandResult]] = None,
    ):
        """Initialize with predetermined responses.

        Args:
            file_contents: A dictionary mapping file paths to their contents.
            http_responses: A dictionary mapping URLs to HttpResponse objects.
            command_results: A dictionary mapping command strings to CommandResult objects.
        """
        self.file_contents = file_contents or {}
        self.http_responses = http_responses or {}
        self.command_results = command_results or {}
        self.written_files: Dict[str, bytes] = {}
        self.logs: List[Tuple[str, str]] = []

    def read_file(self, path: str) -> bytes:
        """Return predetermined file contents for the given path."""
        if path not in self.file_contents:
            raise FileNotFoundError(f"No fake content for {path}")
        return self.file_contents[path]

    def write_file(self, path: str, content: bytes) -> None:
        """Store written content in the written_files dictionary."""
        self.written_files[path] = content

    def http_get(self, url: str, **kwargs: Any) -> HttpResponse:
        """Return predetermined HTTP response for the given URL."""
        if url not in self.http_responses:
            raise ValueError(f"No fake response for GET {url}")
        return self.http_responses[url]

    def http_post(self, url: str, data: Any, **kwargs: Any) -> HttpResponse:
        """Return predetermined HTTP response for the given URL and data."""
        key = f"{url}:{repr(data)}"
        if key not in self.http_responses:
            # Fall back to URL-only key if the specific data key isn't found
            if url not in self.http_responses:
                raise ValueError(f"No fake response for POST {url} with {data}")
            return self.http_responses[url]
        return self.http_responses[key]

    def execute_command(self, cmd: List[str]) -> CommandResult:
        """Return predetermined command result for the given command."""
        cmd_str = " ".join(cmd)
        if cmd_str not in self.command_results:
            raise ValueError(f"No fake result for command: {cmd_str}")
        return self.command_results[cmd_str]

    def log(self, level: str, message: str) -> None:
        """Store log messages in the logs list."""
        self.logs.append((level, message))


class TracingIO(IOContext):
    """Wraps another IO context and records all operations.

    This class implements the IOContext protocol by delegating to another
    IOContext implementation and recording all operations performed.
    """

    def __init__(self, base_ctx: IOContext):
        """Initialize with a base IOContext to delegate to.

        Args:
            base_ctx: The base IOContext to delegate operations to.
        """
        self.base_ctx = base_ctx
        self.trace: List[Tuple[str, Dict[str, Any], Any]] = []

    def read_file(self, path: str) -> bytes:
        """Delegate to base context and record the operation."""
        result = self.base_ctx.read_file(path)
        self.trace.append(("read_file", {"path": path}, result))
        return result

    def write_file(self, path: str, content: bytes) -> None:
        """Delegate to base context and record the operation."""
        self.base_ctx.write_file(path, content)
        self.trace.append(("write_file", {"path": path, "content_size": len(content)}, None))

    def http_get(self, url: str, **kwargs: Any) -> HttpResponse:
        """Delegate to base context and record the operation."""
        result = self.base_ctx.http_get(url, **kwargs)
        self.trace.append(("http_get", {"url": url, **kwargs}, result))
        return result

    def http_post(self, url: str, data: Any, **kwargs: Any) -> HttpResponse:
        """Delegate to base context and record the operation."""
        result = self.base_ctx.http_post(url, data, **kwargs)
        self.trace.append(("http_post", {"url": url, "data": data, **kwargs}, result))
        return result

    def execute_command(self, cmd: List[str]) -> CommandResult:
        """Delegate to base context and record the operation."""
        result = self.base_ctx.execute_command(cmd)
        self.trace.append(("execute_command", {"cmd": cmd}, result))
        return result

    def log(self, level: str, message: str) -> None:
        """Delegate to base context and record the operation."""
        self.base_ctx.log(level, message)
        self.trace.append(("log", {"level": level, "message": message}, None))

    def get_trace(self) -> List[Tuple[str, Dict[str, Any], Any]]:
        """Get the trace of all operations performed.

        Returns:
            A list of tuples containing (operation_name, args, result).
        """
        return self.trace
