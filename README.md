# dotconfig

A Python library that bridges YAML configuration files and environment variables, providing the flexibility to configure applications using either approach.

## Installation

```bash
pip install dotconfig
```

## Quick Start

Just like python-dotenv, dotconfig is designed to be simple to use:

```python
from dotconfig import load_config

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
from dotconfig import load_config

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

## Why dotconfig?

- **Development**: Use readable YAML files for complex configuration
- **Production**: Use environment variables for deployment flexibility
- **Serverless**: Perfect for AWS Lambda, Docker, and other containerized environments
- **12-Factor**: Follows the 12-factor app methodology for configuration
- **Simple**: Drop-in replacement approach - your app code stays clean

## Advanced Usage

For more complex scenarios, you can define custom schemas and transformation rules. See the [Advanced Configuration Guide](docs/advanced.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.