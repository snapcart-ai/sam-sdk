"""SAM SDK — typed Python client for the SAM API."""

from sam_sdk._admin import AdminClient, AsyncAdminClient
from sam_sdk._client import AsyncSAMClient, SAMClient
from sam_sdk._exceptions import (
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    SAMError,
    ServerError,
)
from sam_sdk._types import (
    APIInfo,
    BenchmarkResult,
    BenchmarkStats,
    ChatChoice,
    ChatCompletion,
    ChatMessage,
    ChatUsage,
    CreatedKey,
    EndpointUsage,
    HealthStatus,
    InferenceResult,
    KeyInfo,
    Leaderboard,
    LeaderboardEntry,
    ModelComparison,
    Task,
    TaskList,
    TaskResult,
    UsageStats,
)

__all__ = [
    # Clients
    "SAMClient",
    "AsyncSAMClient",
    "AdminClient",
    "AsyncAdminClient",
    # Exceptions
    "SAMError",
    "AuthenticationError",
    "PermissionError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    # Types
    "APIInfo",
    "BenchmarkResult",
    "BenchmarkStats",
    "ChatChoice",
    "ChatCompletion",
    "ChatMessage",
    "ChatUsage",
    "CreatedKey",
    "EndpointUsage",
    "HealthStatus",
    "InferenceResult",
    "KeyInfo",
    "Leaderboard",
    "LeaderboardEntry",
    "ModelComparison",
    "Task",
    "TaskList",
    "TaskResult",
    "UsageStats",
]
