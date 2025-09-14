"""
Test scenarios for data type handling
"""

from pytest_bdd import scenarios

# Import shared step definitions
import shared_steps

# Load all scenarios from the feature file
scenarios("../features/data_types.feature")
