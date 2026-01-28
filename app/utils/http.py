from __future__ import annotations

import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")

def with_retries(
    fn: Callable[[], T],
    *,
    retries: int = 4,
    base_delay_s: float = 0.6,
    max_delay_s: float = 6.0,
    jitter: float = 0.25,
) -> T:
    """Retry helper with exponential backoff + jitter.
    Retries on exceptions raised by fn.
    """
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt >= retries:
                break
            delay = min(max_delay_s, base_delay_s * (2 ** attempt))
            # jitter in +/- jitter*delay
            delay = max(0.0, delay + random.uniform(-jitter * delay, jitter * delay))
            time.sleep(delay)
    assert last_exc is not None
    raise last_exc
