"""SAMClient and AsyncSAMClient — typed wrappers for the SAM API."""

from __future__ import annotations

from typing import Any

from sam_sdk._transport import _AsyncTransport, _SyncTransport
from sam_sdk._types import (
    APIInfo,
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
)


class SAMClient:
    """Synchronous client for the SAM API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        headers: dict[str, str] = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._transport = _SyncTransport(base_url, headers=headers, timeout=timeout)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> SAMClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    # ── Health ────────────────────────────────────────────────────────────

    def health(self) -> HealthStatus:
        return HealthStatus._from_dict(self._transport.get("/health"))

    def info(self) -> APIInfo:
        return APIInfo._from_dict(self._transport.get("/v1/info"))

    # ── Benchmark ─────────────────────────────────────────────────────────

    def list_tasks(
        self,
        *,
        task_type: str | None = None,
        difficulty: str | None = None,
        split: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> TaskList:
        return TaskList._from_dict(
            self._transport.get(
                "/v1/benchmark/tasks",
                params={
                    "task_type": task_type,
                    "difficulty": difficulty,
                    "split": split,
                    "offset": offset,
                    "limit": limit,
                },
            )
        )

    def get_task(self, task_id: str) -> Task:
        return Task._from_dict(self._transport.get(f"/v1/benchmark/tasks/{task_id}"))

    def benchmark_stats(self) -> BenchmarkStats:
        return BenchmarkStats._from_dict(self._transport.get("/v1/benchmark/stats"))

    # ── Leaderboard ───────────────────────────────────────────────────────

    def leaderboard(self, *, sort_by: str | None = None) -> Leaderboard:
        return Leaderboard._from_dict(
            self._transport.get("/v1/leaderboard", params={"sort_by": sort_by})
        )

    def leaderboard_model(self, model_name: str) -> LeaderboardEntry:
        return LeaderboardEntry._from_dict(
            self._transport.get(f"/v1/leaderboard/{model_name}")
        )

    def compare_models(self, model_a: str, model_b: str) -> ModelComparison:
        return ModelComparison._from_dict(
            self._transport.get(
                "/v1/leaderboard/compare",
                params={"model_a": model_a, "model_b": model_b},
            )
        )

    # ── Inference ─────────────────────────────────────────────────────────

    def _infer(self, path: str, body: dict[str, Any]) -> InferenceResult:
        return InferenceResult._from_dict(self._transport.post(path, json=body))

    def recommend(
        self,
        catalog: list[dict[str, Any]],
        *,
        preferences: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/recommend", {"catalog": catalog, "preferences": preferences or {}, "backend": backend, "model": model})

    def compare(
        self,
        products: list[dict[str, Any]],
        *,
        criteria: list[str] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/compare", {"products": products, "criteria": criteria or [], "backend": backend, "model": model})

    def synthesize(
        self,
        reviews: list[dict[str, Any]],
        *,
        product: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/synthesize", {"reviews": reviews, "product": product or {}, "backend": backend, "model": model})

    def price_analyze(
        self,
        price_history: list[dict[str, Any]],
        *,
        product: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/price/analyze", {"price_history": price_history, "product": product or {}, "backend": backend, "model": model})

    def purchase_decide(
        self,
        options: list[dict[str, Any]],
        *,
        user_profile: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/purchase/decide", {"options": options, "user_profile": user_profile or {}, "backend": backend, "model": model})

    def extract_attributes(
        self,
        description: str,
        *,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/extract/attributes", {"description": description, "backend": backend, "model": model})

    def query_parse(
        self,
        query: str,
        *,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/query/parse", {"query": query, "backend": backend, "model": model})

    def personalize(
        self,
        candidates: list[dict[str, Any]],
        *,
        user_profile: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return self._infer("/v1/personalize", {"candidates": candidates, "user_profile": user_profile or {}, "backend": backend, "model": model})

    # ── Chat ──────────────────────────────────────────────────────────────

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion._from_dict(
            self._transport.post(
                "/v1/chat/completions",
                json={
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "backend": backend,
                    "model": model,
                },
            )
        )

    # ── Evaluation ────────────────────────────────────────────────────────

    def evaluate(self, task_id: str, prediction: dict[str, Any]) -> TaskResult:
        return TaskResult._from_dict(
            self._transport.post(
                "/v1/evaluate/single",
                json={"task_id": task_id, "prediction": prediction},
            )
        )

    def evaluate_batch(
        self, task_ids: list[str], predictions: list[dict[str, Any]]
    ) -> BenchmarkResult:
        return BenchmarkResult._from_dict(
            self._transport.post(
                "/v1/evaluate",
                json={"task_ids": task_ids, "predictions": predictions},
            )
        )


class AsyncSAMClient:
    """Asynchronous client for the SAM API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        headers: dict[str, str] = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._transport = _AsyncTransport(base_url, headers=headers, timeout=timeout)

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> AsyncSAMClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    # ── Health ────────────────────────────────────────────────────────────

    async def health(self) -> HealthStatus:
        return HealthStatus._from_dict(await self._transport.get("/health"))

    async def info(self) -> APIInfo:
        return APIInfo._from_dict(await self._transport.get("/v1/info"))

    # ── Benchmark ─────────────────────────────────────────────────────────

    async def list_tasks(
        self,
        *,
        task_type: str | None = None,
        difficulty: str | None = None,
        split: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> TaskList:
        return TaskList._from_dict(
            await self._transport.get(
                "/v1/benchmark/tasks",
                params={
                    "task_type": task_type,
                    "difficulty": difficulty,
                    "split": split,
                    "offset": offset,
                    "limit": limit,
                },
            )
        )

    async def get_task(self, task_id: str) -> Task:
        return Task._from_dict(await self._transport.get(f"/v1/benchmark/tasks/{task_id}"))

    async def benchmark_stats(self) -> BenchmarkStats:
        return BenchmarkStats._from_dict(await self._transport.get("/v1/benchmark/stats"))

    # ── Leaderboard ───────────────────────────────────────────────────────

    async def leaderboard(self, *, sort_by: str | None = None) -> Leaderboard:
        return Leaderboard._from_dict(
            await self._transport.get("/v1/leaderboard", params={"sort_by": sort_by})
        )

    async def leaderboard_model(self, model_name: str) -> LeaderboardEntry:
        return LeaderboardEntry._from_dict(
            await self._transport.get(f"/v1/leaderboard/{model_name}")
        )

    async def compare_models(self, model_a: str, model_b: str) -> ModelComparison:
        return ModelComparison._from_dict(
            await self._transport.get(
                "/v1/leaderboard/compare",
                params={"model_a": model_a, "model_b": model_b},
            )
        )

    # ── Inference ─────────────────────────────────────────────────────────

    async def _infer(self, path: str, body: dict[str, Any]) -> InferenceResult:
        return InferenceResult._from_dict(await self._transport.post(path, json=body))

    async def recommend(
        self,
        catalog: list[dict[str, Any]],
        *,
        preferences: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/recommend", {"catalog": catalog, "preferences": preferences or {}, "backend": backend, "model": model})

    async def compare(
        self,
        products: list[dict[str, Any]],
        *,
        criteria: list[str] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/compare", {"products": products, "criteria": criteria or [], "backend": backend, "model": model})

    async def synthesize(
        self,
        reviews: list[dict[str, Any]],
        *,
        product: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/synthesize", {"reviews": reviews, "product": product or {}, "backend": backend, "model": model})

    async def price_analyze(
        self,
        price_history: list[dict[str, Any]],
        *,
        product: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/price/analyze", {"price_history": price_history, "product": product or {}, "backend": backend, "model": model})

    async def purchase_decide(
        self,
        options: list[dict[str, Any]],
        *,
        user_profile: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/purchase/decide", {"options": options, "user_profile": user_profile or {}, "backend": backend, "model": model})

    async def extract_attributes(
        self,
        description: str,
        *,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/extract/attributes", {"description": description, "backend": backend, "model": model})

    async def query_parse(
        self,
        query: str,
        *,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/query/parse", {"query": query, "backend": backend, "model": model})

    async def personalize(
        self,
        candidates: list[dict[str, Any]],
        *,
        user_profile: dict[str, Any] | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> InferenceResult:
        return await self._infer("/v1/personalize", {"candidates": candidates, "user_profile": user_profile or {}, "backend": backend, "model": model})

    # ── Chat ──────────────────────────────────────────────────────────────

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        backend: str | None = None,
        model: str | None = None,
    ) -> ChatCompletion:
        return ChatCompletion._from_dict(
            await self._transport.post(
                "/v1/chat/completions",
                json={
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "backend": backend,
                    "model": model,
                },
            )
        )

    # ── Evaluation ────────────────────────────────────────────────────────

    async def evaluate(self, task_id: str, prediction: dict[str, Any]) -> TaskResult:
        return TaskResult._from_dict(
            await self._transport.post(
                "/v1/evaluate/single",
                json={"task_id": task_id, "prediction": prediction},
            )
        )

    async def evaluate_batch(
        self, task_ids: list[str], predictions: list[dict[str, Any]]
    ) -> BenchmarkResult:
        return BenchmarkResult._from_dict(
            await self._transport.post(
                "/v1/evaluate",
                json={"task_ids": task_ids, "predictions": predictions},
            )
        )
