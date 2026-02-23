"""Low-level HTTP transport wrappers around httpx."""

from __future__ import annotations

from typing import Any

import httpx

from sam_sdk._exceptions import raise_for_status


def _strip_none(d: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *d* with all ``None``-valued keys removed."""
    return {k: v for k, v in d.items() if v is not None}


class _SyncTransport:
    """Thin synchronous wrapper around :class:`httpx.Client`."""

    def __init__(self, base_url: str, headers: dict[str, str] | None = None, timeout: float = 30.0) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers=headers or {},
            timeout=timeout,
        )

    # ── request helpers ───────────────────────────────────────────────────

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        params = _strip_none(params) if params else None
        resp = self._client.get(path, params=params)
        return self._handle(resp)

    def post(self, path: str, *, json: dict[str, Any] | None = None) -> Any:
        json = _strip_none(json) if json else None
        resp = self._client.post(path, json=json)
        return self._handle(resp)

    def delete(self, path: str) -> Any:
        resp = self._client.delete(path)
        return self._handle(resp)

    def close(self) -> None:
        self._client.close()

    # ── internals ─────────────────────────────────────────────────────────

    @staticmethod
    def _handle(resp: httpx.Response) -> Any:
        body = resp.json()
        raise_for_status(resp.status_code, body)
        return body


class _AsyncTransport:
    """Thin asynchronous wrapper around :class:`httpx.AsyncClient`."""

    def __init__(self, base_url: str, headers: dict[str, str] | None = None, timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers or {},
            timeout=timeout,
        )

    # ── request helpers ───────────────────────────────────────────────────

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        params = _strip_none(params) if params else None
        resp = await self._client.get(path, params=params)
        return self._handle(resp)

    async def post(self, path: str, *, json: dict[str, Any] | None = None) -> Any:
        json = _strip_none(json) if json else None
        resp = await self._client.post(path, json=json)
        return self._handle(resp)

    async def delete(self, path: str) -> Any:
        resp = await self._client.delete(path)
        return self._handle(resp)

    async def close(self) -> None:
        await self._client.aclose()

    # ── internals ─────────────────────────────────────────────────────────

    @staticmethod
    def _handle(resp: httpx.Response) -> Any:
        body = resp.json()
        raise_for_status(resp.status_code, body)
        return body
