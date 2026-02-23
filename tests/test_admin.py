"""Tests for AdminClient (synchronous)."""

from __future__ import annotations

from sam_sdk._types import CreatedKey, KeyInfo, UsageStats

CREATED_KEY_BODY = {"key_id": "key-abc", "raw_key": "sk-sam-xyz", "tier": "pro"}

KEY_INFO = {
    "key_id": "key-abc",
    "tier": "pro",
    "description": "test",
    "created_at": 1700000000.0,
    "revoked": False,
}

KEYS_BODY = {"keys": [KEY_INFO]}

REVOKE_BODY = {"status": "revoked", "key_id": "key-abc"}

USAGE_BODY = {
    "total_requests": 42,
    "endpoints": {
        "/v1/recommend": {
            "count": 20,
            "avg_latency_ms": 15.0,
            "min_latency_ms": 5.0,
            "max_latency_ms": 50.0,
        }
    },
}


def test_create_key(admin, mock_api):
    mock_api.post("/v1/admin/keys").respond(200, json=CREATED_KEY_BODY)
    result = admin.create_key(tier="pro", description="test")
    assert isinstance(result, CreatedKey)
    assert result.tier == "pro"
    assert result.raw_key == "sk-sam-xyz"


def test_list_keys(admin, mock_api):
    mock_api.get("/v1/admin/keys").respond(200, json=KEYS_BODY)
    result = admin.list_keys()
    assert len(result) == 1
    assert isinstance(result[0], KeyInfo)
    assert result[0].key_id == "key-abc"


def test_revoke_key(admin, mock_api):
    mock_api.delete("/v1/admin/keys/key-abc").respond(200, json=REVOKE_BODY)
    result = admin.revoke_key("key-abc")
    assert result["status"] == "revoked"


def test_usage(admin, mock_api):
    mock_api.get("/v1/usage").respond(200, json=USAGE_BODY)
    result = admin.usage()
    assert isinstance(result, UsageStats)
    assert result.total_requests == 42
    assert result.endpoints["/v1/recommend"].count == 20
