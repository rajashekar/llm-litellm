# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2024-07-14

### Fixed
- Fixed model display in `llm models` list to show full model ID with `litellm/` prefix
- Models now display as `litellm/model-name` instead of `litellm: model-name` for consistency with other plugins

## [0.1.1] - 2024-07-14

### Fixed
- Fixed compatibility with older versions of LLM library (Python 3.8 support)
- Made AsyncChat import optional to support LLM versions that don't have it
- Updated tests to handle optional async functionality

## [0.1.0] - 2024-07-14

### Added
- Initial release of llm-lite plugin
- Support for LiteLLM proxy server integration
- Dynamic model discovery from LiteLLM server
- Environment variable configuration via `LITELLM_URL`
- Optional API key support via `llm keys set litellm`
- Custom commands: `llm litellm models` and `llm litellm status`
- Fallback models when server is unreachable
- Comprehensive test suite with 8 tests
- GitHub Actions workflows for testing and publishing
- Complete documentation with installation and usage guide
- Example scripts and installation helpers

### Features
- Sync and async chat model support
- OpenAI-compatible API integration
- Support for all standard LLM options (temperature, max_tokens, etc.)
- Automatic URL formatting and validation
- Error handling and user-friendly messages

[Unreleased]: https://github.com/rajashekar/llm-litellm/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/rajashekar/llm-litellm/releases/tag/v0.1.1
[0.1.0]: https://github.com/rajashekar/llm-litellm/releases/tag/v0.1.0