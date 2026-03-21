import pytest
from faker import Faker


@pytest.fixture(scope="session", autouse=False)
def fake():
    """Global fixture to provide a Faker instance to all tests."""
    return Faker()
