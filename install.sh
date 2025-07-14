#!/bin/bash

# Installation script for llm-lite plugin

echo "Installing llm-lite plugin..."

# Check if llm is installed
if ! command -v llm &> /dev/null; then
    echo "Error: llm CLI tool is not installed. Please install it first:"
    echo "pip install llm"
    exit 1
fi

# Install the plugin
pip install -e .

if [ $? -eq 0 ]; then
    echo "✅ llm-lite plugin installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Set up your LiteLLM server:"
    echo "   pip install litellm[proxy]"
    echo "   litellm --model gpt-3.5-turbo"
    echo ""
    echo "2. Set the environment variable:"
    echo "   export LITELLM_URL=http://localhost:4000"
    echo ""
    echo "3. (Optional) Set API key if your server requires auth:"
    echo "   llm keys set litellm"
    echo ""
    echo "4. Test the plugin:"
    echo "   llm -m litellm/gpt-3.5-turbo \"Hello, world!\""
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi