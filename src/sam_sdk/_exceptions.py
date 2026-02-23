"""SAM SDK exception hierarchy."""

from __future__ import annotations


class SAMError(Exception):
    """Base exception for all SAM SDK errors."""

    def __init__(self, message: str, status_code: int | None = None, body: object = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class AuthenticationError(SAMError):
    """Raised on 401 Unauthorized."""


class PermissionError(SAMError):  # noqa: A001
    """Raised on 403 Forbidden."""


class NotFoundError(SAMError):
    """Raised on 404 Not Found."""


class RateLimitError(SAMError):
    """Raised on 429 Too Many Requests."""


class ServerError(SAMError):
    """Raised on 5xx responses."""


_STATUS_MAP: dict[int, type[SAMError]] = {
    401: AuthenticationError,
    403: PermissionError,
    404: NotFoundError,
    429: RateLimitError,
}


def raise_for_status(status_code: int, body: object) -> None:
    """Raise the appropriate SAMError subclass for non-2xx responses."""
    if 200 <= status_code < 300:
        return
    detail = ""
    if isinstance(body, dict):
        detail = body.get("detail", str(body))
    else:
        detail = str(body)
    cls = _STATUS_MAP.get(status_code)
    if cls is None and status_code >= 500:
        cls = ServerError
    if cls is None:
        cls = SAMError
    raise cls(detail, status_code=status_code, body=body)
