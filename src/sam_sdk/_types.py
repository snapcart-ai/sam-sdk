"""Frozen dataclasses for SAM API responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Health ────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class HealthStatus:
    status: str

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> HealthStatus:
        return cls(status=d["status"])


@dataclass(frozen=True)
class APIInfo:
    app: str
    version: str
    benchmark: dict[str, Any]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> APIInfo:
        return cls(app=d["app"], version=d["version"], benchmark=d["benchmark"])


# ── Benchmark ─────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Task:
    task_id: str
    task_type: str
    difficulty: str
    input_data: dict[str, Any]
    expected_output: dict[str, Any]
    metadata: dict[str, Any]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> Task:
        return cls(
            task_id=d["task_id"],
            task_type=d["task_type"],
            difficulty=d["difficulty"],
            input_data=d["input_data"],
            expected_output=d["expected_output"],
            metadata=d.get("metadata", {}),
        )


@dataclass(frozen=True)
class TaskList:
    tasks: list[Task]
    total: int
    offset: int
    limit: int

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> TaskList:
        return cls(
            tasks=[Task._from_dict(t) for t in d["tasks"]],
            total=d["total"],
            offset=d["offset"],
            limit=d["limit"],
        )


@dataclass(frozen=True)
class BenchmarkStats:
    total_tasks: int
    task_type_counts: dict[str, int]
    difficulty_counts: dict[str, int]
    splits: list[str]
    task_types: list[str]
    difficulties: list[str]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> BenchmarkStats:
        return cls(
            total_tasks=d["total_tasks"],
            task_type_counts=d["task_type_counts"],
            difficulty_counts=d["difficulty_counts"],
            splits=d["splits"],
            task_types=d["task_types"],
            difficulties=d["difficulties"],
        )


# ── Leaderboard ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class LeaderboardEntry:
    model_name: str
    overall_score: float
    category_scores: dict[str, float]
    difficulty_scores: dict[str, float]
    num_tasks: int
    metadata: dict[str, Any]
    submitted_at: str | None = None

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> LeaderboardEntry:
        return cls(
            model_name=d["model_name"],
            overall_score=d["overall_score"],
            category_scores=d["category_scores"],
            difficulty_scores=d["difficulty_scores"],
            num_tasks=d["num_tasks"],
            metadata=d.get("metadata", {}),
            submitted_at=d.get("submitted_at"),
        )


@dataclass(frozen=True)
class Leaderboard:
    entries: list[LeaderboardEntry]
    total: int
    sort_by: str

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> Leaderboard:
        return cls(
            entries=[LeaderboardEntry._from_dict(e) for e in d["entries"]],
            total=d["total"],
            sort_by=d["sort_by"],
        )


@dataclass(frozen=True)
class ModelComparison:
    models: list[str]
    overall: dict[str, Any]
    by_category: dict[str, Any]
    by_difficulty: dict[str, Any]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> ModelComparison:
        return cls(
            models=d["models"],
            overall=d["overall"],
            by_category=d["by_category"],
            by_difficulty=d["by_difficulty"],
        )


# ── Inference ─────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class InferenceResult:
    task_type: str
    prediction: dict[str, Any]
    model: str
    backend: str
    latency_ms: float

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> InferenceResult:
        return cls(
            task_type=d["task_type"],
            prediction=d["prediction"],
            model=d["model"],
            backend=d["backend"],
            latency_ms=d["latency_ms"],
        )


# ── Chat ──────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> ChatMessage:
        return cls(role=d["role"], content=d["content"])


@dataclass(frozen=True)
class ChatChoice:
    index: int
    message: ChatMessage
    finish_reason: str

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> ChatChoice:
        return cls(
            index=d["index"],
            message=ChatMessage._from_dict(d["message"]),
            finish_reason=d["finish_reason"],
        )


@dataclass(frozen=True)
class ChatUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> ChatUsage:
        return cls(
            prompt_tokens=d["prompt_tokens"],
            completion_tokens=d["completion_tokens"],
            total_tokens=d["total_tokens"],
        )


@dataclass(frozen=True)
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: list[ChatChoice]
    usage: ChatUsage

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> ChatCompletion:
        return cls(
            id=d["id"],
            object=d["object"],
            created=d["created"],
            model=d["model"],
            choices=[ChatChoice._from_dict(c) for c in d["choices"]],
            usage=ChatUsage._from_dict(d["usage"]),
        )


# ── Evaluation ────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class TaskResult:
    task_id: str
    task_type: str
    difficulty: str
    metrics: dict[str, float]
    score: float

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> TaskResult:
        return cls(
            task_id=d["task_id"],
            task_type=d["task_type"],
            difficulty=d["difficulty"],
            metrics=d["metrics"],
            score=d["score"],
        )


@dataclass(frozen=True)
class BenchmarkResult:
    overall_score: float
    category_scores: dict[str, float]
    difficulty_scores: dict[str, float]
    num_tasks: int
    results: list[TaskResult]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> BenchmarkResult:
        return cls(
            overall_score=d["overall_score"],
            category_scores=d["category_scores"],
            difficulty_scores=d["difficulty_scores"],
            num_tasks=d["num_tasks"],
            results=[TaskResult._from_dict(r) for r in d["results"]],
        )


# ── Admin ─────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CreatedKey:
    key_id: str
    raw_key: str
    tier: str

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> CreatedKey:
        return cls(key_id=d["key_id"], raw_key=d["raw_key"], tier=d["tier"])


@dataclass(frozen=True)
class KeyInfo:
    key_id: str
    tier: str
    description: str
    created_at: float
    revoked: bool

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> KeyInfo:
        return cls(
            key_id=d["key_id"],
            tier=d["tier"],
            description=d.get("description", ""),
            created_at=d["created_at"],
            revoked=d["revoked"],
        )


@dataclass(frozen=True)
class EndpointUsage:
    count: int
    avg_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> EndpointUsage:
        return cls(
            count=d["count"],
            avg_latency_ms=d["avg_latency_ms"],
            min_latency_ms=d["min_latency_ms"],
            max_latency_ms=d["max_latency_ms"],
        )


@dataclass(frozen=True)
class UsageStats:
    total_requests: int
    endpoints: dict[str, EndpointUsage]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> UsageStats:
        return cls(
            total_requests=d["total_requests"],
            endpoints={
                k: EndpointUsage._from_dict(v) for k, v in d["endpoints"].items()
            },
        )
