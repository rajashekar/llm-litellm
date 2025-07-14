#!/usr/bin/env python3
"""
Basic usage example for llm-lite plugin.

This script demonstrates how to use the llm-lite plugin programmatically.
"""

import os
import subprocess
import sys


def check_requirements():
    """Check if required environment variables and dependencies are set."""
    if not os.getenv('LITELLM_URL'):
        print("❌ LITELLM_URL environment variable is not set")
        print("   Please set it to your LiteLLM server URL:")
        print("   export LITELLM_URL=http://localhost:4000")
        return False
    
    try:
        result = subprocess.run(['llm', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ LLM CLI tool is not installed")
            print("   Please install it with: pip install llm")
            return False
    except FileNotFoundError:
        print("❌ LLM CLI tool is not found")
        print("   Please install it with: pip install llm")
        return False
    
    return True


def test_server_connection():
    """Test connection to LiteLLM server."""
    print("🔍 Testing LiteLLM server connection...")
    
    try:
        result = subprocess.run(['llm', 'litellm', 'status'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Server check failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False


def list_models():
    """List available models."""
    print("📋 Available models:")
    
    try:
        result = subprocess.run(['llm', 'litellm', 'models'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Failed to list models: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False


def test_basic_query():
    """Test a basic query."""
    print("💬 Testing basic query...")
    
    try:
        result = subprocess.run([
            'llm', '-m', 'litellm/gpt-3.5-turbo', 
            'Say hello and tell me you are working correctly'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Query successful!")
            print(f"Response: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Query failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Query timed out")
        return False
    except Exception as e:
        print(f"❌ Error running query: {e}")
        return False


def main():
    """Main function to run all tests."""
    print("🚀 LLM-Lite Plugin Test Script")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Test server connection
    if not test_server_connection():
        print("\n💡 Make sure your LiteLLM server is running:")
        print("   litellm --model gpt-3.5-turbo")
        sys.exit(1)
    
    # List models
    if not list_models():
        sys.exit(1)
    
    # Test basic query
    if not test_basic_query():
        sys.exit(1)
    
    print("\n🎉 All tests passed! The llm-lite plugin is working correctly.")
    print("\nYou can now use commands like:")
    print("  llm -m litellm/gpt-3.5-turbo 'Your question here'")
    print("  llm -m litellm/claude-3-sonnet 'Another question'")


if __name__ == "__main__":
    main()