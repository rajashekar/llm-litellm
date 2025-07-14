# llm-litellm

[![PyPI](https://img.shields.io/pypi/v/llm-litellm.svg)](https://pypi.org/project/llm-litellm/)
[![Changelog](https://img.shields.io/github/v/release/rajashekar/llm-litellm?include_prereleases&label=changelog)](https://github.com/rajashekar/llm-litellm/releases)
[![Tests](https://github.com/rajashekar/llm-litellm/workflows/Test/badge.svg)](https://github.com/rajashekar/llm-litellm/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rajashekar/llm-litellm/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by [LiteLLM](https://github.com/BerriAI/litellm) proxy server.

LiteLLM is a self-hosted proxy server that provides a unified interface to 100+ LLMs including OpenAI, Anthropic, Cohere, Replicate, PaLM, and more.

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM:
```bash
llm install llm-litellmllm
```

Or install from source:
```bash
pip install -e .
```

## Configuration

### 1. Set up LiteLLM Server

First, you need to have a LiteLLM server running. You can set it up by:

```bash
pip install litellm[proxy]
litellm --model gpt-3.5-turbo
# This starts the server on http://localhost:4000
```

Or use Docker:
```bash
docker run -p 4000:4000 -e OPENAI_API_KEY=your-key ghcr.io/berriai/litellm:main-latest --model gpt-3.5-turbo
```

### 2. Set Environment Variable

Set the `LITELLM_URL` environment variable to point to your LiteLLM server:

```bash
export LITELLM_URL=http://localhost:4000
```

### 3. Set API Key (Optional)

If your LiteLLM server requires authentication, set the API key:

```bash
llm keys set litellm
# Enter your LiteLLM API key when prompted
```

## Usage

Once configured, you can use any model supported by your LiteLLM server.

### List Available Models

To see all available models:
```bash
llm models list
```

You should see models prefixed with `litellm:`:
```
litellm: gpt-3.5-turbo
litellm: gpt-4
litellm: claude-3-sonnet
...
```

You can also use the plugin-specific command:
```bash
llm litellm models
```

### Basic Usage

```bash
# Use a specific model
llm -m litellm/gpt-3.5-turbo "Hello, world!"

# Use with different models
llm -m litellm/claude-3-sonnet "Explain quantum computing"
llm -m litellm/gpt-4 "Write a short story"
```

### Advanced Usage

```bash
# Set temperature and other parameters
llm -m litellm/gpt-3.5-turbo -o temperature 0.9 -o max_tokens 500 "Be creative!"

# Use with streaming
llm -m litellm/gpt-4 "Write a long explanation" --stream

# Conversation mode
llm -m litellm/claude-3-sonnet -c "Let's discuss Python programming"
```

### Model Aliases

You can set shorter aliases for frequently used models:

```bash
llm aliases set gpt4 litellm/gpt-4
llm aliases set claude litellm/claude-3-sonnet
```

Now you can use:
```bash
llm -m gpt4 "Hello!"
llm -m claude "Explain this code" < script.py
```

## Plugin Commands

### Check Server Status

```bash
llm litellm status
```

This will check if your LiteLLM server is running and accessible.

### List Models

```bash
# Human-readable format
llm litellm models

# JSON format
llm litellm models --json
```

## Supported Models

The plugin supports any model that your LiteLLM server is configured to handle. Common models include:

- **OpenAI**: `gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo`
- **Anthropic**: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- **Google**: `gemini-pro`, `gemini-pro-vision`
- **Cohere**: `command-r`, `command-r-plus`
- **Meta**: `llama-2-70b`, `llama-2-13b`
- **Mistral**: `mistral-7b`, `mistral-medium`
- And many more...

Check your LiteLLM server configuration for the exact models available.

## Configuration Options

The plugin supports all standard LLM options:

- `temperature`: Controls randomness (0.0-2.0)
- `max_tokens`: Maximum tokens to generate
- `top_p`: Top-p sampling parameter
- `frequency_penalty`: Frequency penalty (-2.0 to 2.0)
- `presence_penalty`: Presence penalty (-2.0 to 2.0)

Example:
```bash
llm -m litellm/gpt-3.5-turbo \
    -o temperature 0.7 \
    -o max_tokens 1000 \
    -o top_p 0.9 \
    "Generate creative content"
```

## Troubleshooting

### Common Issues

1. **"LITELLM_URL environment variable is required"**
   - Make sure you've set the `LITELLM_URL` environment variable
   - Verify your LiteLLM server is running and accessible

2. **No models showing up**
   - Check server status: `llm litellm status`
   - Verify the URL is correct (should include protocol: http:// or https://)
   - Test the server directly: `curl http://localhost:4000/health`

3. **Connection errors**
   - Check that your LiteLLM server is running
   - Verify firewall settings allow connections to the server
   - Test with: `curl http://localhost:4000/v1/models`

4. **Authentication errors**
   - If your LiteLLM server requires authentication, set the key: `llm keys set litellm`
   - Check your LiteLLM server configuration for authentication requirements

5. **Model not found**
   - Verify the model is configured in your LiteLLM server
   - Check available models: `llm litellm models`
   - Ensure the model name matches exactly

### Debug Mode

For debugging, you can check what models are available:

```bash
# Check server status
llm litellm status

# List all models
llm litellm models --json

# Test a simple query
llm -m litellm/gpt-3.5-turbo "test" -v
```

## Examples

### Setting up with Different Providers

#### OpenAI Models
```bash
export OPENAI_API_KEY=your-key
litellm --model gpt-3.5-turbo --model gpt-4
export LITELLM_URL=http://localhost:4000
llm -m litellm/gpt-3.5-turbo "Hello!"
```

#### Anthropic Models
```bash
export ANTHROPIC_API_KEY=your-key
litellm --model claude-3-sonnet --model claude-3-haiku
export LITELLM_URL=http://localhost:4000
llm -m litellm/claude-3-sonnet "Hello!"
```

#### Multiple Providers
```bash
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
litellm --model gpt-4 --model claude-3-sonnet --model gemini-pro
export LITELLM_URL=http://localhost:4000
llm -m litellm/gpt-4 "Compare yourself to Claude"
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-litellm
python3 -m venv venv
source venv/bin/activate
```

Install the plugin in development mode:
```bash
pip install -e '.[test]'
```

To run the tests:
```bash
pytest
```

## License

Apache License 2.0