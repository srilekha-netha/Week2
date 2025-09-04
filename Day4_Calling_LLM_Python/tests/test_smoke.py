from __future__ import annotations
import os
import pytest

has_key = bool(os.getenv("GROQ_API_KEY"))

@pytest.mark.skipif(not has_key, reason="No GROQ_API_KEY set")
def test_env_present():
    assert has_key
