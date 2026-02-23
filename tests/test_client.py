"""Tests for SAMClient (synchronous)."""

from __future__ import annotations

import httpx
import respx

from sam_sdk import SAMClient
from sam_sdk._types import (
    BenchmarkResult,
    BenchmarkStats,
    ChatCompletion,
    HealthStatus,
    InferenceResult,
    Leaderboard,
    LeaderboardEntry,
    ModelComparison,
    Task,
    TaskList,
    TaskResult,
    APIInfo,
)

BASE = "http://test-sam.local"

# ── Fixtures ──────────────────────────────────────────────────────────────────

HEALTH_BODY = {"status": "ok"}

INFO_BODY = {"app": "SAM API", "version": "0.1.0", "benchmark": {"tasks": 1200}}

TASK_BODY = {
    "task_id": "t1",
    "task_type": "product_recommendation",
    "difficulty": "easy",
    "input_data": {"catalog": []},
    "expected_output": {"ranked": []},
    "metadata": {},
}

TASK_LIST_BODY = {"tasks": [TASK_BODY], "total": 1, "offset": 0, "limit": 50}

STATS_BODY = {
    "total_tasks": 1200,
    "task_type_counts": {"product_recommendation": 150},
    "difficulty_counts": {"easy": 400},
    "splits": ["train", "validation", "test"],
    "task_types": ["product_recommendation"],
    "difficulties": ["easy", "medium", "hard"],
}

LEADERBOARD_ENTRY = {
    "model_name": "gpt-4",
    "overall_score": 0.75,
    "category_scores": {"product_recommendation": 0.8},
    "difficulty_scores": {"easy": 0.9},
    "num_tasks": 100,
    "metadata": {},
    "submitted_at": "2025-01-01",
}

LEADERBOARD_BODY = {"entries": [LEADERBOARD_ENTRY], "total": 1, "sort_by": "overall"}

COMPARE_BODY = {
    "models": ["gpt-4", "gpt-3.5"],
    "overall": {"gpt-4": 0.75, "gpt-3.5": 0.60},
    "by_category": {},
    "by_difficulty": {},
}

INFERENCE_BODY = {
    "task_type": "product_recommendation",
    "prediction": {"ranked_products": ["p1"]},
    "model": "heuristic",
    "backend": "baseline",
    "latency_ms": 5.2,
}

CHAT_BODY = {
    "id": "chatcmpl-abc",
    "object": "chat.completion",
    "created": 1700000000,
    "model": "heuristic",
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "Hello!"},
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
}

TASK_RESULT_BODY = {
    "task_id": "t1",
    "task_type": "product_recommendation",
    "difficulty": "easy",
    "metrics": {"ndcg": 0.8},
    "score": 0.8,
}

BENCHMARK_RESULT_BODY = {
    "overall_score": 0.75,
    "category_scores": {"product_recommendation": 0.8},
    "difficulty_scores": {"easy": 0.9},
    "num_tasks": 1,
    "results": [TASK_RESULT_BODY],
}


# ── Health ────────────────────────────────────────────────────────────────────


def test_health(client, mock_api):
    mock_api.get("/health").respond(200, json=HEALTH_BODY)
    result = client.health()
    assert isinstance(result, HealthStatus)
    assert result.status == "ok"


def test_info(client, mock_api):
    mock_api.get("/v1/info").respond(200, json=INFO_BODY)
    result = client.info()
    assert isinstance(result, APIInfo)
    assert result.version == "0.1.0"


# ── Benchmark ─────────────────────────────────────────────────────────────────


def test_list_tasks(client, mock_api):
    mock_api.get("/v1/benchmark/tasks").respond(200, json=TASK_LIST_BODY)
    result = client.list_tasks()
    assert isinstance(result, TaskList)
    assert result.total == 1
    assert result.tasks[0].task_id == "t1"


def test_list_tasks_with_filters(client, mock_api):
    route = mock_api.get("/v1/benchmark/tasks").respond(200, json=TASK_LIST_BODY)
    client.list_tasks(task_type="product_recommendation", difficulty="easy", split="train", offset=10, limit=5)
    req = route.calls.last.request
    assert b"task_type=product_recommendation" in req.url.raw_path
    assert b"difficulty=easy" in req.url.raw_path


def test_get_task(client, mock_api):
    mock_api.get("/v1/benchmark/tasks/t1").respond(200, json=TASK_BODY)
    result = client.get_task("t1")
    assert isinstance(result, Task)
    assert result.task_type == "product_recommendation"


def test_benchmark_stats(client, mock_api):
    mock_api.get("/v1/benchmark/stats").respond(200, json=STATS_BODY)
    result = client.benchmark_stats()
    assert isinstance(result, BenchmarkStats)
    assert result.total_tasks == 1200


# ── Leaderboard ───────────────────────────────────────────────────────────────


def test_leaderboard(client, mock_api):
    mock_api.get("/v1/leaderboard").respond(200, json=LEADERBOARD_BODY)
    result = client.leaderboard()
    assert isinstance(result, Leaderboard)
    assert result.entries[0].model_name == "gpt-4"


def test_leaderboard_model(client, mock_api):
    mock_api.get("/v1/leaderboard/gpt-4").respond(200, json=LEADERBOARD_ENTRY)
    result = client.leaderboard_model("gpt-4")
    assert isinstance(result, LeaderboardEntry)
    assert result.overall_score == 0.75


def test_compare_models(client, mock_api):
    mock_api.get("/v1/leaderboard/compare").respond(200, json=COMPARE_BODY)
    result = client.compare_models("gpt-4", "gpt-3.5")
    assert isinstance(result, ModelComparison)
    assert "gpt-4" in result.models


# ── Inference ─────────────────────────────────────────────────────────────────


def test_recommend(client, mock_api):
    mock_api.post("/v1/recommend").respond(200, json=INFERENCE_BODY)
    result = client.recommend(catalog=[{"product_id": "p1", "name": "Widget", "price": 9.99, "rating": 4.5}])
    assert isinstance(result, InferenceResult)
    assert result.task_type == "product_recommendation"


def test_compare_products(client, mock_api):
    mock_api.post("/v1/compare").respond(200, json=INFERENCE_BODY)
    result = client.compare(products=[{"id": "p1"}, {"id": "p2"}], criteria=["price"])
    assert isinstance(result, InferenceResult)


def test_synthesize(client, mock_api):
    mock_api.post("/v1/synthesize").respond(200, json=INFERENCE_BODY)
    result = client.synthesize(reviews=[{"text": "Great!", "rating": 5}])
    assert isinstance(result, InferenceResult)


def test_price_analyze(client, mock_api):
    mock_api.post("/v1/price/analyze").respond(200, json=INFERENCE_BODY)
    result = client.price_analyze(price_history=[{"date": "2025-01-01", "price": 9.99}])
    assert isinstance(result, InferenceResult)


def test_purchase_decide(client, mock_api):
    mock_api.post("/v1/purchase/decide").respond(200, json=INFERENCE_BODY)
    result = client.purchase_decide(options=[{"id": "p1", "price": 9.99}])
    assert isinstance(result, InferenceResult)


def test_extract_attributes(client, mock_api):
    mock_api.post("/v1/extract/attributes").respond(200, json=INFERENCE_BODY)
    result = client.extract_attributes("A red cotton t-shirt, size M")
    assert isinstance(result, InferenceResult)


def test_query_parse(client, mock_api):
    mock_api.post("/v1/query/parse").respond(200, json=INFERENCE_BODY)
    result = client.query_parse("cheap wireless headphones under $50")
    assert isinstance(result, InferenceResult)


def test_personalize(client, mock_api):
    mock_api.post("/v1/personalize").respond(200, json=INFERENCE_BODY)
    result = client.personalize(candidates=[{"id": "p1"}], user_profile={"age": 25})
    assert isinstance(result, InferenceResult)


# ── Chat ──────────────────────────────────────────────────────────────────────


def test_chat(client, mock_api):
    mock_api.post("/v1/chat/completions").respond(200, json=CHAT_BODY)
    result = client.chat(messages=[{"role": "user", "content": "Hi"}])
    assert isinstance(result, ChatCompletion)
    assert result.choices[0].message.content == "Hello!"
    assert result.usage.total_tokens == 12


# ── Evaluation ────────────────────────────────────────────────────────────────


def test_evaluate(client, mock_api):
    mock_api.post("/v1/evaluate/single").respond(200, json=TASK_RESULT_BODY)
    result = client.evaluate("t1", prediction={"ranked_products": ["p1"]})
    assert isinstance(result, TaskResult)
    assert result.score == 0.8


def test_evaluate_batch(client, mock_api):
    mock_api.post("/v1/evaluate").respond(200, json=BENCHMARK_RESULT_BODY)
    result = client.evaluate_batch(
        task_ids=["t1"],
        predictions=[{"ranked_products": ["p1"]}],
    )
    assert isinstance(result, BenchmarkResult)
    assert result.overall_score == 0.75
    assert len(result.results) == 1
