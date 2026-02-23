# SAM SDK

Typed Python client for the [SAM (Shopping Agent Model) API](https://github.com/snapcart-ai/sam-api).

## Installation

```bash
pip install sam-sdk
```

## Quick Start

```python
from sam_sdk import SAMClient

client = SAMClient("https://api.snapcart.cc", api_key="sk-sam-...")

# Health check
status = client.health()
print(status.status)  # "ok"

# Product recommendation
result = client.recommend(
    catalog=[
        {"product_id": "p1", "name": "Widget", "price": 9.99, "rating": 4.5},
        {"product_id": "p2", "name": "Gadget", "price": 19.99, "rating": 4.0},
    ],
    preferences={"category": "electronics"},
)
print(result.prediction)

# Chat completions (OpenAI-compatible)
completion = client.chat(
    messages=[{"role": "user", "content": "Compare these two products"}],
    temperature=0.7,
)
print(completion.choices[0].message.content)
```

## Async Usage

```python
import asyncio
from sam_sdk import AsyncSAMClient

async def main():
    async with AsyncSAMClient("https://api.snapcart.cc") as client:
        status = await client.health()
        print(status.status)

asyncio.run(main())
```

## Admin Client

```python
from sam_sdk import AdminClient

admin = AdminClient("https://api.snapcart.cc", admin_key="<your-admin-key>")

# Create an API key
key = admin.create_key(tier="pro", description="CI pipeline")
print(key.raw_key)

# View usage
stats = admin.usage()
print(stats.total_requests)
```

## Error Handling

```python
from sam_sdk import SAMClient, NotFoundError, RateLimitError

client = SAMClient("https://api.snapcart.cc")

try:
    task = client.get_task("nonexistent")
except NotFoundError as e:
    print(f"Task not found: {e}")
except RateLimitError as e:
    print(f"Rate limited (status {e.status_code}): {e}")
```

## License

MIT
