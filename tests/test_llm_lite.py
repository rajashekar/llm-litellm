import pytest
import os
from unittest.mock import patch, MagicMock
import json
from llm_lite import get_litellm_url, get_litellm_models, LiteLLMChat


def test_get_litellm_url_missing():
    """Test that get_litellm_url raises error when LITELLM_URL is not set."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="LITELLM_URL environment variable is required"):
            get_litellm_url()


def test_get_litellm_url_formatting():
    """Test URL formatting in get_litellm_url."""
    # Test URL without /v1
    with patch.dict(os.environ, {'LITELLM_URL': 'http://localhost:4000'}):
        assert get_litellm_url() == 'http://localhost:4000/v1'
    
    # Test URL with trailing slash
    with patch.dict(os.environ, {'LITELLM_URL': 'http://localhost:4000/'}):
        assert get_litellm_url() == 'http://localhost:4000/v1'
    
    # Test URL already with /v1
    with patch.dict(os.environ, {'LITELLM_URL': 'http://localhost:4000/v1'}):
        assert get_litellm_url() == 'http://localhost:4000/v1'


@patch('llm_lite.httpx.get')
@patch('llm_lite.llm.get_key')
@patch('llm_lite.get_litellm_url')
def test_get_litellm_models_success(mock_get_url, mock_get_key, mock_httpx_get):
    """Test successful model fetching."""
    mock_get_url.return_value = 'http://localhost:4000/v1'
    mock_get_key.return_value = 'test-key'
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {"id": "gpt-3.5-turbo", "object": "model"},
            {"id": "gpt-4", "object": "model"}
        ]
    }
    mock_httpx_get.return_value = mock_response
    
    models = get_litellm_models()
    
    assert len(models) == 2
    assert models[0]["id"] == "gpt-3.5-turbo"
    assert models[1]["id"] == "gpt-4"
    
    mock_httpx_get.assert_called_once_with(
        'http://localhost:4000/v1/models',
        headers={'Authorization': 'Bearer test-key'},
        timeout=10.0
    )


@patch('llm_lite.httpx.get')
@patch('llm_lite.llm.get_key')
@patch('llm_lite.get_litellm_url')
def test_get_litellm_models_no_auth(mock_get_url, mock_get_key, mock_httpx_get):
    """Test model fetching without authentication."""
    mock_get_url.return_value = 'http://localhost:4000/v1'
    mock_get_key.return_value = None
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [{"id": "gpt-3.5-turbo", "object": "model"}]
    }
    mock_httpx_get.return_value = mock_response
    
    models = get_litellm_models()
    
    assert len(models) == 1
    mock_httpx_get.assert_called_once_with(
        'http://localhost:4000/v1/models',
        headers={},
        timeout=10.0
    )


@patch('llm_lite.httpx.get')
@patch('llm_lite.llm.get_key')
@patch('llm_lite.get_litellm_url')
def test_get_litellm_models_fallback(mock_get_url, mock_get_key, mock_httpx_get):
    """Test fallback models when server is unreachable."""
    mock_get_url.return_value = 'http://localhost:4000/v1'
    mock_get_key.return_value = None
    mock_httpx_get.side_effect = Exception("Connection failed")
    
    models = get_litellm_models()
    
    # Should return default models
    assert len(models) >= 4
    model_ids = [model["id"] for model in models]
    assert "gpt-3.5-turbo" in model_ids
    assert "gpt-4" in model_ids
    assert "claude-3-sonnet" in model_ids
    assert "claude-3-haiku" in model_ids


def test_litellm_chat_model():
    """Test LiteLLMChat model initialization."""
    model = LiteLLMChat(
        model_id="litellm/gpt-3.5-turbo",
        model_name="gpt-3.5-turbo",
        api_base="http://localhost:4000/v1"
    )
    
    assert model.model_id == "litellm/gpt-3.5-turbo"
    assert model.model_name == "gpt-3.5-turbo"
    assert model.api_base == "http://localhost:4000/v1"
    assert str(model) == "litellm: gpt-3.5-turbo"
    assert model.needs_key == "litellm"
    assert model.key_env_var == "LITELLM_KEY"


@patch('llm_lite.get_litellm_models')
@patch('llm_lite.get_litellm_url')
def test_register_models_success(mock_get_url, mock_get_models):
    """Test successful model registration."""
    mock_get_url.return_value = 'http://localhost:4000/v1'
    mock_get_models.return_value = [
        {"id": "gpt-3.5-turbo", "object": "model"},
        {"id": "claude-3-sonnet", "object": "model"}
    ]
    
    from llm_lite import register_models
    
    mock_register = MagicMock()
    register_models(mock_register)
    
    # Should register 2 models (each with chat and async chat)
    assert mock_register.call_count == 2
    
    # Check first model registration
    first_call_args = mock_register.call_args_list[0][0]
    chat_model, async_chat_model = first_call_args
    
    assert isinstance(chat_model, LiteLLMChat)
    assert chat_model.model_id == "litellm/gpt-3.5-turbo"
    assert chat_model.model_name == "gpt-3.5-turbo"


@patch('llm_lite.get_litellm_url')
def test_register_models_no_url(mock_get_url):
    """Test model registration when LITELLM_URL is not set."""
    mock_get_url.side_effect = ValueError("LITELLM_URL environment variable is required")
    
    from llm_lite import register_models
    
    mock_register = MagicMock()
    register_models(mock_register)
    
    # Should not register any models
    mock_register.assert_not_called()