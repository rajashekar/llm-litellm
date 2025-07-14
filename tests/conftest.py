import pytest
import os
from unittest.mock import patch


@pytest.fixture
def clean_env():
    """Fixture to provide a clean environment for tests."""
    with patch.dict(os.environ, {}, clear=True):
        yield


@pytest.fixture
def mock_litellm_env():
    """Fixture to provide a mock LiteLLM environment."""
    with patch.dict(os.environ, {'LITELLM_URL': 'http://localhost:4000'}):
        yield