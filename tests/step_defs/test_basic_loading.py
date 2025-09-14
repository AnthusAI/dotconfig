"""
Test scenarios for basic YAML loading functionality
"""

from pytest_bdd import scenarios

# Import shared step definitions
import shared_steps

# Load all scenarios from the feature file
scenarios("../features/basic_loading.feature")
