"""AdminClient and AsyncAdminClient — typed wrappers for SAM admin endpoints."""

from __future__ import annotations

from sam_sdk._transport import _AsyncTransport, _SyncTransport
from sam_sdk._types import CreatedKey, KeyInfo, UsageStats


class AdminClient:
    """Synchronous client for SAM API admin endpoints."""

    def __init__(
        self,
        base_url: str,
        admin_key: str,
        timeout: float = 30.0,
    ) -> None:
        headers = {"Authorization": f"Bearer {admin_key}"}
        self._transport = _SyncTransport(base_url, headers=headers, timeout=timeout)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> AdminClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    # ── Key management ────────────────────────────────────────────────────

    def create_key(self, *, tier: str = "free", description: str = "") -> CreatedKey:
        return CreatedKey._from_dict(
            self._transport.post(
                "/v1/admin/keys",
                json={"tier": tier, "description": description},
            )
        )

    def list_keys(self) -> list[KeyInfo]:
        data = self._transport.get("/v1/admin/keys")
        return [KeyInfo._from_dict(k) for k in data["keys"]]

    def revoke_key(self, key_id: str) -> dict[str, str]:
        return self._transport.delete(f"/v1/admin/keys/{key_id}")

    # ── Usage ─────────────────────────────────────────────────────────────

    def usage(self) -> UsageStats:
        return UsageStats._from_dict(self._transport.get("/v1/usage"))


class AsyncAdminClient:
    """Asynchronous client for SAM API admin endpoints."""

    def __init__(
        self,
        base_url: str,
        admin_key: str,
        timeout: float = 30.0,
    ) -> None:
        headers = {"Authorization": f"Bearer {admin_key}"}
        self._transport = _AsyncTransport(base_url, headers=headers, timeout=timeout)

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> AsyncAdminClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    # ── Key management ────────────────────────────────────────────────────

    async def create_key(self, *, tier: str = "free", description: str = "") -> CreatedKey:
        return CreatedKey._from_dict(
            await self._transport.post(
                "/v1/admin/keys",
                json={"tier": tier, "description": description},
            )
        )

    async def list_keys(self) -> list[KeyInfo]:
        data = await self._transport.get("/v1/admin/keys")
        return [KeyInfo._from_dict(k) for k in data["keys"]]

    async def revoke_key(self, key_id: str) -> dict[str, str]:
        return await self._transport.delete(f"/v1/admin/keys/{key_id}")

    # ── Usage ─────────────────────────────────────────────────────────────

    async def usage(self) -> UsageStats:
        return UsageStats._from_dict(await self._transport.get("/v1/usage"))
