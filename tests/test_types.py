"""Tests for SAM SDK dataclass types."""

from sam_sdk._types import (
    ChatCompletion,
    HealthStatus,
    InferenceResult,
    TaskList,
)


def test_health_status_from_dict():
    hs = HealthStatus._from_dict({"status": "ok"})
    assert hs.status == "ok"


def test_task_list_from_dict():
    tl = TaskList._from_dict(
        {
            "tasks": [
                {
                    "task_id": "t1",
                    "task_type": "product_recommendation",
                    "difficulty": "easy",
                    "input_data": {"key": "val"},
                    "expected_output": {"out": 1},
                    "metadata": {},
                }
            ],
            "total": 1,
            "offset": 0,
            "limit": 50,
        }
    )
    assert len(tl.tasks) == 1
    assert tl.tasks[0].task_id == "t1"
    assert tl.total == 1


def test_inference_result_from_dict():
    ir = InferenceResult._from_dict(
        {
            "task_type": "product_recommendation",
            "prediction": {"items": ["a"]},
            "model": "heuristic",
            "backend": "baseline",
            "latency_ms": 12.5,
        }
    )
    assert ir.latency_ms == 12.5
    assert ir.prediction == {"items": ["a"]}


def test_chat_completion_from_dict():
    cc = ChatCompletion._from_dict(
        {
            "id": "chatcmpl-1",
            "object": "chat.completion",
            "created": 1700000000,
            "model": "heuristic",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "hi"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 1,
                "total_tokens": 6,
            },
        }
    )
    assert cc.choices[0].message.content == "hi"
    assert cc.usage.total_tokens == 6
