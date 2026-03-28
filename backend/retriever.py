from backend.embedder import Embedder
from backend.exceptions import EmptyKnowledgeBaseError
from backend.models import RetrievalResult
from backend.vector_store import VectorStore

_LOW_CONFIDENCE_THRESHOLD = 0.3


class Retriever:
    """Thin orchestration layer that embeds a query and delegates to VectorStore."""

    def __init__(self, embedder: Embedder, vector_store: VectorStore) -> None:
        self._embedder = embedder
        self._vector_store = vector_store

    def retrieve(self, query: str, k: int = 5) -> RetrievalResult:
        """
        Returns RetrievalResult with scored_chunks and low_confidence flag
        (True when all scores < 0.3).

        Raises EmptyKnowledgeBaseError if the vector store contains no chunks.
        """
        # Embed the query — embed() returns a list of embeddings; take the first
        query_embedding = self._embedder.embed([query])[0]

        # Delegate to VectorStore; EmptyKnowledgeBaseError propagates naturally
        scored_chunks = self._vector_store.search(query_embedding, k)

        # Set low_confidence when no chunks returned or all scores are below threshold
        low_confidence = all(
            sc.score < _LOW_CONFIDENCE_THRESHOLD for sc in scored_chunks
        ) if scored_chunks else True

        return RetrievalResult(scored_chunks=scored_chunks, low_confidence=low_confidence)
