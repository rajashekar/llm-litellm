import os
import httpx
import llm
from llm.default_plugins.openai_models import Chat, AsyncChat
from pydantic import Field
from typing import Optional
import json
import click


class _mixin:
    class Options(Chat.Options):
        pass

    def build_kwargs(self, prompt, stream):
        kwargs = super().build_kwargs(prompt, stream)
        return kwargs


class LiteLLMChat(_mixin, Chat):
    needs_key = "litellm"
    key_env_var = "LITELLM_KEY"

    def __init__(self, model_id, model_name, api_base, **kwargs):
        self._model_name = model_name
        super().__init__(model_id, api_base=api_base, **kwargs)
        # Set model_name after parent initialization
        self._model_name = model_name

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value

    def __str__(self):
        return "litellm: {}".format(self._model_name)


class LiteLLMAsyncChat(_mixin, AsyncChat):
    needs_key = "litellm"
    key_env_var = "LITELLM_KEY"

    def __init__(self, model_id, model_name, api_base, **kwargs):
        self._model_name = model_name
        super().__init__(model_id, api_base=api_base, **kwargs)
        # Set model_name after parent initialization
        self._model_name = model_name

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value

    def __str__(self):
        return "litellm: {}".format(self._model_name)


def get_litellm_url():
    """Get LiteLLM URL from environment variable."""
    litellm_url = os.getenv("LITELLM_URL")
    if not litellm_url:
        raise ValueError(
            "LITELLM_URL environment variable is required. "
            "Please set it to your LiteLLM server URL (e.g., http://localhost:4000)"
        )
    
    # Ensure URL ends with /v1 for OpenAI-compatible API
    if not litellm_url.endswith('/v1'):
        if litellm_url.endswith('/'):
            litellm_url = litellm_url + 'v1'
        else:
            litellm_url = litellm_url + '/v1'
    
    return litellm_url


def get_litellm_models():
    """Fetch available models from LiteLLM server."""
    try:
        litellm_url = get_litellm_url()
        
        # Get API key if available
        key = llm.get_key("", "litellm", "LITELLM_KEY")
        headers = {}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        
        response = httpx.get(f"{litellm_url}/models", headers=headers, timeout=10.0)
        response.raise_for_status()
        
        models_data = response.json()
        if "data" in models_data:
            return models_data["data"]
        else:
            return models_data
    except Exception as e:
        # If we can't fetch models, return some common defaults
        print(f"Warning: Could not fetch models from LiteLLM server: {e}")
        return [
            {"id": "gpt-3.5-turbo", "object": "model"},
            {"id": "gpt-4", "object": "model"},
            {"id": "claude-3-sonnet", "object": "model"},
            {"id": "claude-3-haiku", "object": "model"},
        ]


@llm.hookimpl
def register_models(register):
    # Check if LITELLM_URL is set
    try:
        litellm_url = get_litellm_url()
    except ValueError:
        # If LITELLM_URL is not set, don't register any models
        return
    
    # Get available models from LiteLLM server
    models = get_litellm_models()
    
    for model in models:
        model_id = model.get("id", "unknown")
        model_name = model_id
        
        kwargs = dict(
            model_id=f"litellm/{model_id}",
            model_name=model_name,
            api_base=litellm_url,
        )
        
        # Create model instances
        chat_model = LiteLLMChat(**kwargs)
        async_chat_model = LiteLLMAsyncChat(**kwargs)
        
        register(chat_model, async_chat_model)


@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def litellm():
        "Commands relating to the llm-lite plugin"

    @litellm.command()
    @click.option("json_", "--json", is_flag=True, help="Output as JSON")
    def models(json_):
        "List available LiteLLM models"
        try:
            all_models = get_litellm_models()
            if json_:
                click.echo(json.dumps(all_models, indent=2))
            else:
                # Custom format
                for model in all_models:
                    model_id = model.get("id", "unknown")
                    click.echo(f"- id: {model_id}")
                    if "object" in model:
                        click.echo(f"  type: {model['object']}")
                    if "owned_by" in model:
                        click.echo(f"  owned_by: {model['owned_by']}")
                    click.echo()
        except Exception as e:
            click.echo(f"Error fetching models: {e}", err=True)

    @litellm.command()
    def status():
        "Check LiteLLM server status"
        try:
            litellm_url = get_litellm_url()
            
            # Get API key if available
            key = llm.get_key("", "litellm", "LITELLM_KEY")
            headers = {}
            if key:
                headers["Authorization"] = f"Bearer {key}"
            
            # Try to hit the health endpoint
            health_url = litellm_url.replace('/v1', '/health')
            response = httpx.get(health_url, headers=headers, timeout=5.0)
            
            if response.status_code == 200:
                click.echo(f"✅ LiteLLM server is running at {litellm_url}")
                try:
                    health_data = response.json()
                    if isinstance(health_data, dict):
                        for key, value in health_data.items():
                            click.echo(f"   {key}: {value}")
                except:
                    click.echo(f"   Status: {response.status_code}")
            else:
                click.echo(f"⚠️  LiteLLM server responded with status {response.status_code}")
                
        except ValueError as e:
            click.echo(f"❌ Configuration error: {e}", err=True)
        except Exception as e:
            click.echo(f"❌ Cannot connect to LiteLLM server: {e}", err=True)