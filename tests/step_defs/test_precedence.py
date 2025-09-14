"""
Test scenarios for environment variable precedence
"""

from pytest_bdd import scenarios

# Import shared step definitions
import shared_steps

# Load all scenarios from the feature file
scenarios("../features/precedence.feature")
