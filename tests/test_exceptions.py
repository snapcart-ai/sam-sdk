"""Tests for SAM SDK exception mapping."""

import httpx
import pytest
import respx

from sam_sdk import (
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    SAMClient,
    SAMError,
    ServerError,
)

BASE = "http://test-sam.local"


@pytest.mark.parametrize(
    "status,exc_cls",
    [
        (401, AuthenticationError),
        (403, PermissionError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, ServerError),
        (422, SAMError),
    ],
)
def test_status_code_mapping(status, exc_cls):
    with respx.mock(base_url=BASE) as router:
        router.get("/health").respond(status, json={"detail": "oops"})
        client = SAMClient(base_url=BASE)
        with pytest.raises(exc_cls) as exc_info:
            client.health()
        assert exc_info.value.status_code == status
        client.close()


def test_error_body_preserved():
    with respx.mock(base_url=BASE) as router:
        router.get("/health").respond(404, json={"detail": "not found"})
        client = SAMClient(base_url=BASE)
        with pytest.raises(NotFoundError) as exc_info:
            client.health()
        assert exc_info.value.body == {"detail": "not found"}
        assert "not found" in str(exc_info.value)
        client.close()
