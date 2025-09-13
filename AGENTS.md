# AGENTS.md - Guide for AI Coding Agents

This document provides guidance for AI coding agents working on the dotconfig project.

## Project Overview

**dotconfig** is a Python library that bridges YAML configuration files and environment variables. It allows applications to be configured via either YAML files (development) or environment variables (production/serverless), providing maximum deployment flexibility.

## Core Philosophy

1. **Simplicity First**: The API should be as simple as python-dotenv - just import and call `load_config()`
2. **Deployment Flexibility**: Same app code works with YAML files OR environment variables
3. **12-Factor Compliance**: Environment variables take precedence for production deployments
4. **Serverless Ready**: Perfect for AWS Lambda, Docker containers, and other stateless environments

## Key Design Principles

### Bidirectional Configuration
Unlike libraries that only resolve env vars IN YAML files, we need:
- YAML → Environment Variables (load YAML, set env vars)
- Environment Variables → Configuration (read env vars, build config)

### Flattening Strategy
Transform nested YAML structures into flat environment variable names:
```yaml
database:
  host: localhost
  port: 5432
```
Becomes: `APP_DATABASE_HOST`, `APP_DATABASE_PORT`

### Type Handling
Environment variables are strings, but YAML supports rich types. Handle:
- Booleans: `true`/`false` strings
- Numbers: String representations
- Lists: JSON or comma-separated strings
- Objects: JSON strings

## Code Architecture

### Core Modules
- `loader.py`: Main `load_config()` function and ConfigLoader class
- `transformer.py`: YAML ↔ environment variable transformation logic
- `schema.py`: Configuration schema definition and validation
- `utils.py`: Helper functions for type conversion and key transformation

### API Design Goals
```python
# Simple usage (like dotenv)
from dotconfig import load_config
load_config('config.yaml', prefix='APP')

# Advanced usage with schema
from dotconfig import ConfigLoader, Schema
loader = ConfigLoader(schema=my_schema)
config = loader.load_from_yaml('config.yaml')
```

## Implementation Guidelines

### Testing Strategy
- Unit tests for each transformation function
- Integration tests with real YAML files
- Environment variable precedence testing
- Type conversion edge cases
- Schema validation testing

### Dependencies
Keep minimal:
- PyYAML (required for YAML parsing)
- No other required dependencies
- Optional dependencies for advanced features

### Error Handling
- Clear error messages for malformed YAML
- Helpful warnings for type conversion issues
- Graceful fallbacks when files don't exist

## Development Workflow

1. **Start with Tests**: Write tests first for new features
2. **Maintain Backward Compatibility**: API changes should be additive
3. **Documentation**: Update README examples for any API changes
4. **Performance**: Profile with large configuration files

## Common Patterns

### Environment Variable Naming
- Use uppercase letters and underscores
- Configurable prefix (default: no prefix)
- Nested keys joined with underscores: `parent_child_key`

### Precedence Rules
1. Explicitly set environment variables (highest)
2. YAML file values
3. Schema defaults (if defined)

## Security Considerations

- Never log configuration values (may contain secrets)
- Support for secret management integration
- Clear documentation about file permissions for YAML configs

## Future Roadmap

- JSON configuration file support
- Integration with popular frameworks (Flask, Django, FastAPI)
- Configuration validation and type checking
- Hot-reloading for development environments