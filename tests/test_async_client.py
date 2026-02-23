"""Tests for AsyncSAMClient and AsyncAdminClient."""

from __future__ import annotations

import pytest

from sam_sdk._types import CreatedKey, HealthStatus, InferenceResult, TaskList, UsageStats

HEALTH_BODY = {"status": "ok"}

TASK_LIST_BODY = {
    "tasks": [
        {
            "task_id": "t1",
            "task_type": "product_recommendation",
            "difficulty": "easy",
            "input_data": {},
            "expected_output": {},
            "metadata": {},
        }
    ],
    "total": 1,
    "offset": 0,
    "limit": 50,
}

INFERENCE_BODY = {
    "task_type": "product_recommendation",
    "prediction": {"ranked_products": ["p1"]},
    "model": "heuristic",
    "backend": "baseline",
    "latency_ms": 5.0,
}

CREATED_KEY_BODY = {"key_id": "key-abc", "raw_key": "sk-sam-xyz", "tier": "free"}

USAGE_BODY = {"total_requests": 10, "endpoints": {}}


@pytest.mark.asyncio
async def test_async_health(async_client, mock_api):
    mock_api.get("/health").respond(200, json=HEALTH_BODY)
    result = await async_client.health()
    assert isinstance(result, HealthStatus)
    assert result.status == "ok"
    await async_client.close()


@pytest.mark.asyncio
async def test_async_list_tasks(async_client, mock_api):
    mock_api.get("/v1/benchmark/tasks").respond(200, json=TASK_LIST_BODY)
    result = await async_client.list_tasks()
    assert isinstance(result, TaskList)
    assert result.total == 1
    await async_client.close()


@pytest.mark.asyncio
async def test_async_recommend(async_client, mock_api):
    mock_api.post("/v1/recommend").respond(200, json=INFERENCE_BODY)
    result = await async_client.recommend(catalog=[{"product_id": "p1"}])
    assert isinstance(result, InferenceResult)
    await async_client.close()


@pytest.mark.asyncio
async def test_async_admin_create_key(async_admin, mock_api):
    mock_api.post("/v1/admin/keys").respond(200, json=CREATED_KEY_BODY)
    result = await async_admin.create_key()
    assert isinstance(result, CreatedKey)
    assert result.key_id == "key-abc"
    await async_admin.close()


@pytest.mark.asyncio
async def test_async_admin_usage(async_admin, mock_api):
    mock_api.get("/v1/usage").respond(200, json=USAGE_BODY)
    result = await async_admin.usage()
    assert isinstance(result, UsageStats)
    assert result.total_requests == 10
    await async_admin.close()
