"""
Simple non-BDD tests to verify core functionality works
"""

import os
import tempfile
from pathlib import Path
import pytest
from dotconfig import load_config, ConfigLoader


@pytest.fixture(autouse=True)
def clean_env():
    """Clean environment variables before each test"""
    original_env = dict(os.environ)

    # Clear test-related env vars
    test_vars = [
        key
        for key in os.environ.keys()
        if any(
            prefix in key.upper()
            for prefix in [
                "DATABASE",
                "API",
                "CACHE",
                "APP",
                "STRING",
                "INTEGER",
                "FLOAT",
                "BOOLEAN",
                "NULL",
                "EMPTY",
                "SIMPLE",
                "MIXED",
                "NESTED",
                "MYAPP",
            ]
        )
    ]
    for var in test_vars:
        os.environ.pop(var, None)

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def test_load_simple_yaml():
    """Test loading simple YAML configuration"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("database_host: localhost\ndatabase_port: 5432\napi_key: secret123")
        yaml_file = f.name

    result = load_config(yaml_file)

    assert os.getenv("DATABASE_HOST") == "localhost"
    assert os.getenv("DATABASE_PORT") == "5432"
    assert os.getenv("API_KEY") == "secret123"


def test_load_nested_yaml():
    """Test loading nested YAML configuration"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret
api:
  timeout: 30
  retries: 3""")
        yaml_file = f.name

    result = load_config(yaml_file)

    assert os.getenv("DATABASE_HOST") == "localhost"
    assert os.getenv("DATABASE_PORT") == "5432"
    assert os.getenv("DATABASE_CREDENTIALS_USERNAME") == "admin"
    assert os.getenv("DATABASE_CREDENTIALS_PASSWORD") == "secret"
    assert os.getenv("API_TIMEOUT") == "30"
    assert os.getenv("API_RETRIES") == "3"


def test_load_with_prefix():
    """Test loading configuration with prefix"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""database:
  host: localhost
  port: 5432""")
        yaml_file = f.name

    result = load_config(yaml_file, prefix="MYAPP")

    assert os.getenv("MYAPP_DATABASE_HOST") == "localhost"
    assert os.getenv("MYAPP_DATABASE_PORT") == "5432"


def test_data_types():
    """Test data type handling"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write('''string_value: hello world
integer_value: 42
float_value: 3.14
boolean_true: true
boolean_false: false
null_value: null
empty_string: ""''')
        yaml_file = f.name

    result = load_config(yaml_file)

    assert os.getenv("STRING_VALUE") == "hello world"
    assert os.getenv("INTEGER_VALUE") == "42"
    assert os.getenv("FLOAT_VALUE") == "3.14"
    assert os.getenv("BOOLEAN_TRUE") == "true"
    assert os.getenv("BOOLEAN_FALSE") == "false"
    assert os.getenv("NULL_VALUE") == ""
    assert os.getenv("EMPTY_STRING") == ""


def test_list_values():
    """Test list value handling"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""simple_list:
  - item1
  - item2
  - item3
mixed_list:
  - string
  - 42
  - true""")
        yaml_file = f.name

    result = load_config(yaml_file)

    assert os.getenv("SIMPLE_LIST") == "item1,item2,item3"
    assert os.getenv("MIXED_LIST") == "string,42,true"


def test_environment_variable_precedence():
    """Test that environment variables override YAML values"""
    # Set env var first
    os.environ["DATABASE_HOST"] = "production-db.example.com"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""database:
  host: localhost
  port: 5432""")
        yaml_file = f.name

    result = load_config(yaml_file)

    # Env var should win
    assert os.getenv("DATABASE_HOST") == "production-db.example.com"
    assert os.getenv("DATABASE_PORT") == "5432"


def test_config_loader():
    """Test ConfigLoader class without setting environment variables"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""database:
  host: localhost
  port: 5432""")
        yaml_file = f.name

    loader = ConfigLoader()
    config = loader.load_from_yaml(yaml_file)

    assert config == {"database": {"host": "localhost", "port": 5432}}
    # Should not set environment variables
    assert os.getenv("DATABASE_HOST") is None