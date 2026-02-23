"""Shared fixtures for SAM SDK tests."""

from __future__ import annotations

import pytest
import respx

from sam_sdk import AdminClient, AsyncAdminClient, AsyncSAMClient, SAMClient

BASE = "http://test-sam.local"


@pytest.fixture()
def mock_api():
    """Yield a started respx mock router scoped to BASE."""
    with respx.mock(base_url=BASE) as router:
        yield router


@pytest.fixture()
def client(mock_api):
    with SAMClient(base_url=BASE, api_key="sk-sam-test") as c:
        yield c


@pytest.fixture()
def async_client(mock_api):
    return AsyncSAMClient(base_url=BASE, api_key="sk-sam-test")


@pytest.fixture()
def admin(mock_api):
    with AdminClient(base_url=BASE, admin_key="admin-secret") as a:
        yield a


@pytest.fixture()
def async_admin(mock_api):
    return AsyncAdminClient(base_url=BASE, admin_key="admin-secret")
