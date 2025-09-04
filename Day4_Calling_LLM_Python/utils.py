from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential_jitter
from config import CACHE_DIR

# --- tiny file cache ---
def _hash_key(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

class SimpleCache:
    def __init__(self, cache_dir: str = CACHE_DIR):
        self.dir = Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.dir / f"{_hash_key(key)}.json"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        p = self._path(key)
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return None
        return None

    def set(self, key: str, value: Dict[str, Any]) -> None:
        p = self._path(key)
        p.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

# --- retry policy (4 attempts, exp backoff + jitter) ---
# In newer tenacity, multiplier is replaced by exp_base
retry_policy = retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential_jitter(exp_base=2, max=8),  # exp_base acts like multiplier
    reraise=True,
)

def make_cache_key(**kwargs: Any) -> str:
    return json.dumps(kwargs, sort_keys=True, ensure_ascii=False)
