import pytest
from faker import Faker
from faker.providers import BaseProvider

from app.database import Base, engine
from app.services.embeddings import EmbeddingsService
from app.services.ingestion import IngestionService
from app.services.vector_store import VectorStoreService


@pytest.fixture(autouse=True)
def setup_db():

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


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


@pytest.fixture(scope="session")
def embeddings_service():
    """Global fixture to provide an EmbeddingsService instance to all tests."""
    return EmbeddingsService()


@pytest.fixture(scope="session")
def ingestion_service(embeddings_service, vector_store_service):
    """Global fixture to provide an IngestionService instance to all tests."""
    return IngestionService(embeddings_service, vector_store_service)
