"""
Test scenarios for advanced configuration scenarios
"""

from pytest_bdd import scenarios

# Import shared step definitions
import shared_steps

# Load all scenarios from the feature file
scenarios("../features/advanced_config.feature")