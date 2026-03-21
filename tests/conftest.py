import pytest
from faker import Faker
from faker.providers import BaseProvider

from app.database import engine
from app.services.vector_store import VectorStoreService


class VectorProvider(BaseProvider):
    """Custom provider for generating vector embeddings."""

    def vector(self, dims: int = 384) -> list[float]:
        """Generates a random vector of floats of a given dimension."""

        return [float(self.generator.pyfloat(min_value=-1, max_value=1)) for _ in range(dims)]


@pytest.fixture(scope="session")
def fake():
    """Global fixture to provide a localized Faker instance with custom providers."""
    f = Faker("pt_BR")
    f.add_provider(VectorProvider)
    return f


@pytest.fixture(scope="session")
def vector_store_service():
    """Global fixture to provide a VectorStoreService instance to all tests."""
    return VectorStoreService(engine)
