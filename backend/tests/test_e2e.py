# Feature: rag-investment-analysis, E2E: five investment queries
"""
End-to-end acceptance test for the RAG investment analysis pipeline.

Ingests an investment textbook PDF and verifies that each of the five
required investment queries returns at least one chunk with score > 0.3.

The test is marked with `pytest.mark.e2e` so it can be excluded from
unit test runs via: pytest -m "not e2e"

A PDF must be available at the path specified by the TEST_PDF_PATH env var,
or at tests/fixtures/investment.pdf relative to the backend directory.
If no PDF is found the test is skipped automatically.
"""

import io
import os

import chromadb
import pytest

FIVE_QUERIES = [
    "how to deal with brokerage houses?",
    "what is theory of diversification?",
    "how to become intelligent investor?",
    "how to do business valuation?",
    "what is putting all eggs in one basket analogy?",
]

SCORE_THRESHOLD = 0.3


def _find_pdf_path() -> str | None:
    """Return the path to the investment PDF, or None if not found."""
    # 1. Explicit env var
    env_path = os.environ.get("TEST_PDF_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2. Conventional fixture location relative to this file
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "investment.pdf")
    if os.path.isfile(fixture_path):
        return fixture_path

    return None


def _build_ephemeral_vector_store() -> "VectorStore":  # noqa: F821
    """Return a VectorStore backed by a fresh in-memory ChromaDB client."""
    import uuid
    from backend.vector_store import _ChromaBackend, VectorStore

    client = chromadb.EphemeralClient()
    col_name = f"e2e_{uuid.uuid4().hex}"
    collection = client.get_or_create_collection(
        name=col_name,
        metadata={"hnsw:space": "cosine"},
    )

    backend = _ChromaBackend.__new__(_ChromaBackend)
    backend._client = client
    backend._collection = collection
    backend._COLLECTION_NAME = col_name

    store = VectorStore.__new__(VectorStore)
    store._backend = backend
    return store


@pytest.mark.e2e
def test_five_investment_queries_return_relevant_chunks():
    """
    Full pipeline acceptance test.

    Validates: Requirements 8.2, 8.3
    """
    pdf_path = _find_pdf_path()
    if pdf_path is None:
        pytest.skip("No investment PDF available for e2e test")

    # --- Ingestion phase ---
    from backend.ingester import PDFIngester
    from backend.chunker import Chunker
    from backend.embedder import Embedder
    from backend.retriever import Retriever

    ingester = PDFIngester()
    chunker = Chunker(max_tokens=512, overlap_tokens=50)
    embedder = Embedder()
    vector_store = _build_ephemeral_vector_store()

    with open(pdf_path, "rb") as f:
        pages = ingester.ingest(f)

    chunks = chunker.chunk(pages)
    assert chunks, "Chunker produced no chunks from the PDF"

    texts = [c.text for c in chunks]
    embeddings = embedder.embed(texts)
    vector_store.upsert(chunks, embeddings)

    # --- Query phase ---
    retriever = Retriever(embedder=embedder, vector_store=vector_store)

    for query in FIVE_QUERIES:
        result = retriever.retrieve(query, k=5)
        top_score = max((sc.score for sc in result.scored_chunks), default=0.0)
        assert top_score > SCORE_THRESHOLD, (
            f"Query '{query}' returned no chunk with score > {SCORE_THRESHOLD}. "
            f"Top score was {top_score:.4f}."
        )
