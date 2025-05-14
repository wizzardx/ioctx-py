"""
ioctx - A structured effects system for testable side effects in Python.

This module defines the core Protocol and data classes for the ioctx library.
"""

from typing import Any, Dict, List, Optional, Protocol


class HttpResponse:
    """Represents an HTTP response."""

    def __init__(self, status_code: int, text: str, headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}


class CommandResult:
    """Represents the result of executing a command."""

    def __init__(self, return_code: int, stdout: str, stderr: str):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr


class IOContext(Protocol):
    """Protocol defining the interface for IO operations.

    This protocol establishes a consistent interface for various IO operations,
    enabling different implementations to handle these operations in different ways
    (e.g., real operations, simulated responses, etc.).
    """

    def read_file(self, path: str) -> bytes:
        """Read a file and return its contents as bytes.

        Args:
            path: The path to the file to read.

        Returns:
            The contents of the file as bytes.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read due to permissions.
        """
        ...

    def write_file(self, path: str, content: bytes) -> None:
        """Write content to a file at the specified path.

        Args:
            path: The path where the file should be written.
            content: The content to write to the file.

        Raises:
            PermissionError: If the file cannot be written due to permissions.
            IOError: If there's an error writing to the file.
        """
        ...

    def http_get(self, url: str, **kwargs: Any) -> HttpResponse:
        """Perform an HTTP GET request.

        Args:
            url: The URL to request.
            **kwargs: Additional arguments to pass to the HTTP client.

        Returns:
            An HttpResponse object containing the response.

        Raises:
            ValueError: If the URL is invalid.
            ConnectionError: If there's an error connecting to the server.
        """
        ...

    def http_post(self, url: str, data: Any, **kwargs: Any) -> HttpResponse:
        """Perform an HTTP POST request.

        Args:
            url: The URL to request.
            data: The data to send in the request body.
            **kwargs: Additional arguments to pass to the HTTP client.

        Returns:
            An HttpResponse object containing the response.

        Raises:
            ValueError: If the URL is invalid.
            ConnectionError: If there's an error connecting to the server.
        """
        ...

    def execute_command(self, cmd: List[str]) -> CommandResult:
        """Execute a shell command.

        Args:
            cmd: The command to execute as a list of strings.

        Returns:
            A CommandResult object containing the result of the command.

        Raises:
            FileNotFoundError: If the command executable cannot be found.
            PermissionError: If the command cannot be executed due to permissions.
        """
        ...

    def log(self, level: str, message: str) -> None:
        """Log a message with the specified level.

        Args:
            level: The log level (e.g., "debug", "info", "warning", "error").
            message: The message to log.
        """
        ...
