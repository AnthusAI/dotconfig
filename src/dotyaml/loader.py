"""
Core loading functionality for yamlenv
"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any, Union

from .transformer import flatten_dict, unflatten_env_vars


def load_config(
    yaml_path: Optional[Union[str, Path]] = None,
    prefix: str = "",
    override: bool = False,
) -> Dict[str, str]:
    """
    Load configuration from YAML file and set environment variables.

    Args:
        yaml_path: Path to YAML configuration file. If None, only reads existing env vars.
        prefix: Prefix for environment variable names (e.g., 'APP' -> 'APP_DATABASE_HOST')
        override: If True, override existing environment variables

    Returns:
        Dictionary of all configuration values that were set
    """
    config = {}

    if yaml_path and Path(yaml_path).exists():
        # Load and parse YAML file
        with open(yaml_path, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)

        if yaml_data:
            # Transform nested structure to flat env var names
            flat_config = flatten_dict(yaml_data, prefix)

            # Set environment variables with precedence handling
            for key, value in flat_config.items():
                # Check if env var already exists and override is False
                if not override and key in os.environ:
                    # Keep existing env var, but track it in config
                    config[key] = os.environ[key]
                else:
                    # Set new env var
                    os.environ[key] = value
                    config[key] = value

    return config


class ConfigLoader:
    """
    Advanced configuration loader with schema support
    """

    def __init__(self, prefix: str = "", schema: Optional[Dict[str, Any]] = None):
        self.prefix = prefix
        self.schema = schema

    def load_from_yaml(self, yaml_path: Union[str, Path]) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not Path(yaml_path).exists():
            return {}

        with open(yaml_path, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)

        return yaml_data or {}

    def load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        # Get all environment variables
        env_vars = dict(os.environ)

        # Convert back to nested structure
        return unflatten_env_vars(env_vars, self.prefix)

    def set_env_vars(self, config: Dict[str, Any], override: bool = False) -> None:
        """Set environment variables from configuration dictionary"""
        # Flatten the configuration
        flat_config = flatten_dict(config, self.prefix)

        # Set environment variables
        for key, value in flat_config.items():
            if override or key not in os.environ:
                os.environ[key] = value
