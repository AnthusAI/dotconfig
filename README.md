# dotyaml

A Python library that bridges YAML configuration files and environment variables, providing the flexibility to configure applications using either approach.

## Installation

```bash
pip install dotyaml
```

For `.env` file support, also install python-dotenv:

```bash
pip install dotyaml python-dotenv
```

## Quick Start

Just like python-dotenv, dotyaml is designed to be simple to use:

```python
from dotyaml import load_config

# Load configuration from YAML file and set environment variables
load_config('config.yaml')

# Now your app can access configuration via environment variables
import os
db_host = os.getenv('APP_DATABASE_HOST')
```

## Basic Usage

### 1. Create a YAML configuration file

**config.yaml:**
```yaml
database:
  host: localhost
  port: 5432
  name: myapp
api:
  timeout: 30
  retries: 3
```

### 2. Load configuration in your Python application

```python
from dotyaml import load_config

# This will set environment variables based on your YAML structure
load_config('config.yaml', prefix='APP')

# Environment variables are now available:
# APP_DATABASE_HOST=localhost
# APP_DATABASE_PORT=5432
# APP_DATABASE_NAME=myapp
# APP_API_TIMEOUT=30
# APP_API_RETRIES=3
```

### 3. Use environment variables in your application

```python
import os

# Your application code remains simple and flexible
database_config = {
    'host': os.getenv('APP_DATABASE_HOST'),
    'port': int(os.getenv('APP_DATABASE_PORT')),
    'name': os.getenv('APP_DATABASE_NAME')
}
```

## Alternative: Environment Variables Only

Your application works the same way even without a YAML file:

```bash
# Set environment variables directly
export APP_DATABASE_HOST=prod-db.example.com
export APP_DATABASE_PORT=5432
export APP_DATABASE_NAME=production
export APP_API_TIMEOUT=60
export APP_API_RETRIES=5
```

```python
# Your application code doesn't change
import os
database_config = {
    'host': os.getenv('APP_DATABASE_HOST'),
    'port': int(os.getenv('APP_DATABASE_PORT')),
    'name': os.getenv('APP_DATABASE_NAME')
}
```

## Advanced Usage

### Environment Variable Precedence

Environment variables always take precedence over YAML values:

```python
# YAML file has database.host: localhost
# But environment variable is set:
os.environ['APP_DATABASE_HOST'] = 'prod-db.example.com'

load_config('config.yaml', prefix='APP')
# Result: APP_DATABASE_HOST=prod-db.example.com (env var wins)
```

### Force Override

Override existing environment variables with YAML values:

```python
load_config('config.yaml', prefix='APP', override=True)
```

### ConfigLoader for Advanced Use Cases

```python
from dotyaml import ConfigLoader

# Load configuration without setting environment variables
loader = ConfigLoader(prefix='APP')
config = loader.load_from_yaml('config.yaml')  # Returns dict

# Load configuration from environment variables only
env_config = loader.load_from_env()

# Set environment variables from configuration dict
loader.set_env_vars(config)
```

### Integration with python-dotenv

dotyaml works perfectly with python-dotenv for `.env` file support. Since dotconfig respects existing environment variables, you can use both together:

```python
from dotenv import load_dotenv
from dotyaml import load_config

# Load .env file first (if it exists)
load_dotenv()

# Then load YAML config - respects .env values
load_config('config.yaml', prefix='APP')
```

**Precedence order** (highest to lowest):
1. Existing environment variables (including from `.env`)
2. YAML configuration file values
3. Default values (if using schemas)

This pattern gives you maximum flexibility:
- **Development**: Use `.env` for secrets and local overrides
- **Staging**: Mix `.env` and YAML as needed
- **Production**: Use environment variables only

### Data Type Handling

dotyaml automatically handles various YAML data types:

- **Strings**: Passed through as-is
- **Numbers**: Converted to string representations
- **Booleans**: Converted to `"true"`/`"false"`
- **Lists**: Converted to comma-separated strings
- **Null values**: Converted to empty strings

## License

MIT License - see [LICENSE](LICENSE) file for details.