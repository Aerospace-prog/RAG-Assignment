"""
Checkpoint tests for all backend components.
Verifies that each module imports correctly and core logic works without external APIs.
"""
import io
import math
import uuid
import pytest

from backend.models import PageText, Chunk, ScoredChunk, RetrievalResult, GeneratedResponse, StoredRecord
from backend.exceptions import (
    UnsupportedFileError, NoExtractableTextError, EmptyContentError,
    EmbeddingModelError, WriteError, EmptyKnowledgeBaseError, LLMUnavailableError,
)


# ---------------------------------------------------------------------------
# models.py
# ---------------------------------------------------------------------------

class TestModels:
    def test_page_text(self):
        pt = PageText(page_number=1, text="hello")
        assert pt.page_number == 1
        assert pt.text == "hello"

    def test_chunk(self):
        c = Chunk(id="abc", text="text", page_number=2, char_offset=10)
        assert c.id == "abc"
        assert c.char_offset == 10

    def test_scored_chunk(self):
        c = Chunk(id="x", text="t", page_number=1, char_offset=0)
        sc = ScoredChunk(chunk=c, score=0.85)
        assert sc.score == 0.85

    def test_retrieval_result(self):
        rr = RetrievalResult(scored_chunks=[], low_confidence=True)
        assert rr.low_confidence is True

    def test_generated_response(self):
        gr = GeneratedResponse(answer="ans", citations=[1, 2], low_confidence=False)
        assert gr.citations == [1, 2]

    def test_stored_record(self):
        c = Chunk(id="y", text="t", page_number=1, char_offset=0)
        sr = StoredRecord(chunk=c, embedding=[0.1, 0.2])
        assert sr.embedding == [0.1, 0.2]


# ---------------------------------------------------------------------------
# exceptions.py
# ---------------------------------------------------------------------------

class TestExceptions:
    def test_unsupported_file_error(self):
        with pytest.raises(UnsupportedFileError):
            raise UnsupportedFileError("bad file")

    def test_no_extractable_text_error(self):
        with pytest.raises(NoExtractableTextError):
            raise NoExtractableTextError("no text")

    def test_empty_content_error(self):
        with pytest.raises(EmptyContentError):
            raise EmptyContentError("empty")

    def test_embedding_model_error(self):
        with pytest.raises(EmbeddingModelError):
            raise EmbeddingModelError("model down")

    def test_write_error_message(self):
        err = WriteError("chunk-123")
        assert "chunk-123" in str(err)

    def test_empty_knowledge_base_error(self):
        with pytest.raises(EmptyKnowledgeBaseError):
            raise EmptyKnowledgeBaseError("empty kb")

    def test_llm_unavailable_error(self):
        with pytest.raises(LLMUnavailableError):
            raise LLMUnavailableError("llm down")


# ---------------------------------------------------------------------------
# ingester.py
# ---------------------------------------------------------------------------

def _make_simple_pdf(text_per_page: list[str]) -> bytes:
    """Create a minimal valid PDF with given text on each page."""
    from reportlab.pdfgen import canvas  # type: ignore
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    for text in text_per_page:
        c.drawString(72, 720, text)
        c.showPage()
    c.save()
    return buf.getvalue()


def _make_simple_pdf_pypdf(text_per_page: list[str]) -> bytes:
    """Create a minimal valid PDF using pypdf writer."""
    import pypdf
    writer = pypdf.PdfWriter()
    for text in text_per_page:
        page = writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


class TestPDFIngester:
    def test_invalid_bytes_raises_unsupported(self):
        from backend.ingester import PDFIngester
        ingester = PDFIngester()
        with pytest.raises(UnsupportedFileError):
            ingester.ingest(io.BytesIO(b"not a pdf at all"))

    def test_empty_bytes_raises_unsupported(self):
        from backend.ingester import PDFIngester
        ingester = PDFIngester()
        with pytest.raises(UnsupportedFileError):
            ingester.ingest(io.BytesIO(b""))

    def test_blank_pdf_raises_no_extractable_text(self):
        """A PDF with blank pages should raise NoExtractableTextError."""
        from backend.ingester import PDFIngester
        ingester = PDFIngester()
        pdf_bytes = _make_simple_pdf_pypdf([""])
        with pytest.raises(NoExtractableTextError):
            ingester.ingest(io.BytesIO(pdf_bytes))

    def test_returns_page_text_list(self):
        """A PDF with extractable text returns a list of PageText."""
        try:
            from reportlab.pdfgen import canvas as _c  # noqa: F401
        except ImportError:
            pytest.skip("reportlab not installed; skipping text extraction test")
        from backend.ingester import PDFIngester
        ingester = PDFIngester()
        pdf_bytes = _make_simple_pdf(["Hello world", "Page two"])
        result = ingester.ingest(io.BytesIO(pdf_bytes))
        assert len(result) == 2
        assert all(isinstance(p, PageText) for p in result)
        assert result[0].page_number == 1
        assert result[1].page_number == 2


# ---------------------------------------------------------------------------
# chunker.py
# ---------------------------------------------------------------------------

class TestChunker:
    def test_empty_pages_raises_empty_content_error(self):
        from backend.chunker import Chunker
        chunker = Chunker()
        with pytest.raises(EmptyContentError):
            chunker.chunk([PageText(page_number=1, text="")])

    def test_whitespace_only_raises_empty_content_error(self):
        from backend.chunker import Chunker
        chunker = Chunker()
        with pytest.raises(EmptyContentError):
            chunker.chunk([PageText(page_number=1, text="   \n\t  ")])

    def test_short_text_produces_single_chunk(self):
        from backend.chunker import Chunker
        chunker = Chunker(max_tokens=512, overlap_tokens=50)
        pages = [PageText(page_number=1, text="This is a short text.")]
        chunks = chunker.chunk(pages)
        assert len(chunks) == 1
        assert chunks[0].page_number == 1
        assert chunks[0].char_offset == 0
        assert chunks[0].id  # non-empty UUID

    def test_chunk_ids_are_unique(self):
        from backend.chunker import Chunker
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        # Generate text that will produce multiple chunks
        word = "investment " * 60  # ~60 tokens per repeat
        long_text = word * 20  # ~1200 tokens → at least 2 chunks with 512 max
        pages = [PageText(page_number=1, text=long_text)]
        chunker = Chunker(max_tokens=512, overlap_tokens=50)
        chunks = chunker.chunk(pages)
        ids = [c.id for c in chunks]
        assert len(ids) == len(set(ids)), "Chunk IDs must be unique"

    def test_all_chunks_within_token_limit(self):
        from backend.chunker import Chunker
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        long_text = "word " * 2000  # ~2000 tokens
        pages = [PageText(page_number=1, text=long_text)]
        chunker = Chunker(max_tokens=512, overlap_tokens=50)
        chunks = chunker.chunk(pages)
        for chunk in chunks:
            token_count = len(enc.encode(chunk.text))
            assert token_count <= 512, f"Chunk exceeds 512 tokens: {token_count}"

    def test_chunk_metadata_non_null(self):
        from backend.chunker import Chunker
        pages = [PageText(page_number=3, text="Some text on page three.")]
        chunker = Chunker()
        chunks = chunker.chunk(pages)
        for chunk in chunks:
            assert chunk.page_number is not None
            assert chunk.char_offset is not None
            assert chunk.id is not None


# ---------------------------------------------------------------------------
# embedder.py — tested with mocked model to avoid API calls
# ---------------------------------------------------------------------------

class TestEmbedder:
    def test_raises_embedding_model_error_after_3_failures(self, monkeypatch):
        from backend.embedder import Embedder
        embedder = Embedder()
        call_count = 0

        def failing_embed(texts):
            nonlocal call_count
            call_count += 1
            raise RuntimeError("model down")

        monkeypatch.setattr(embedder, "_embed_openai", failing_embed)
        monkeypatch.setenv("EMBEDDING_MODEL", "openai")
        # Patch sleep to avoid waiting
        monkeypatch.setattr("backend.embedder.time.sleep", lambda s: None)

        with pytest.raises(EmbeddingModelError):
            embedder.embed(["test text"])

        assert call_count == 3

    def test_retries_on_transient_failure(self, monkeypatch):
        from backend.embedder import Embedder
        embedder = Embedder()
        call_count = 0

        def flaky_embed(texts):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RuntimeError("transient error")
            return [[0.1, 0.2, 0.3] for _ in texts]

        monkeypatch.setattr(embedder, "_embed_openai", flaky_embed)
        monkeypatch.setenv("EMBEDDING_MODEL", "openai")
        monkeypatch.setattr("backend.embedder.time.sleep", lambda s: None)

        result = embedder.embed(["hello"])
        assert result == [[0.1, 0.2, 0.3]]
        assert call_count == 2

    def test_consistent_dimensionality(self, monkeypatch):
        from backend.embedder import Embedder
        embedder = Embedder()

        def mock_embed(texts):
            return [[0.1, 0.2, 0.3] for _ in texts]

        monkeypatch.setattr(embedder, "_embed_openai", mock_embed)
        monkeypatch.setenv("EMBEDDING_MODEL", "openai")

        result = embedder.embed(["text one", "text two", "text three"])
        dims = [len(v) for v in result]
        assert len(set(dims)) == 1, "All embeddings must have the same dimensionality"


# ---------------------------------------------------------------------------
# vector_store.py — tested with ChromaDB in-memory (ephemeral client)
# ---------------------------------------------------------------------------

class TestVectorStore:
    """Uses an ephemeral ChromaDB client to avoid touching disk."""

    def _make_store(self, monkeypatch):
        """Return a VectorStore backed by a fresh in-memory ChromaDB client."""
        import chromadb
        from backend.vector_store import _ChromaBackend, VectorStore

        # Each call creates a brand-new ephemeral client so collections don't bleed
        client = chromadb.EphemeralClient()
        col_name = f"test_{uuid.uuid4().hex}"
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

    def _make_chunk(self, page=1, text="sample text"):
        return Chunk(id=str(uuid.uuid4()), text=text, page_number=page, char_offset=0)

    def _unit_vec(self, dim=3, idx=0):
        v = [0.0] * dim
        v[idx] = 1.0
        return v

    def test_empty_store_raises_empty_knowledge_base(self, monkeypatch):
        store = self._make_store(monkeypatch)
        with pytest.raises(EmptyKnowledgeBaseError):
            store.search([0.1, 0.2, 0.3], k=5)

    def test_upsert_and_search_round_trip(self, monkeypatch):
        store = self._make_store(monkeypatch)
        chunk = self._make_chunk(page=1, text="investment strategy")
        embedding = [0.1, 0.9, 0.0]
        store.upsert([chunk], [embedding])

        results = store.search(embedding, k=1)
        assert len(results) == 1
        assert results[0].chunk.id == chunk.id
        assert results[0].chunk.text == chunk.text
        assert results[0].chunk.page_number == chunk.page_number

    def test_search_returns_min_k_n_results(self, monkeypatch):
        store = self._make_store(monkeypatch)
        chunks = [self._make_chunk(page=i, text=f"text {i}") for i in range(3)]
        embeddings = [self._unit_vec(3, i) for i in range(3)]
        store.upsert(chunks, embeddings)

        # k=2, N=3 → should return 2
        results = store.search(self._unit_vec(3, 0), k=2)
        assert len(results) == 2

        # k=10, N=3 → should return 3
        results = store.search(self._unit_vec(3, 0), k=10)
        assert len(results) == 3

    def test_search_results_ordered_descending(self, monkeypatch):
        store = self._make_store(monkeypatch)
        chunks = [self._make_chunk(page=i, text=f"text {i}") for i in range(3)]
        embeddings = [self._unit_vec(3, i) for i in range(3)]
        store.upsert(chunks, embeddings)

        results = store.search(self._unit_vec(3, 0), k=3)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_replace_all_clears_old_data(self, monkeypatch):
        store = self._make_store(monkeypatch)
        old_chunk = self._make_chunk(page=1, text="old data")
        store.upsert([old_chunk], [[0.1, 0.2, 0.3]])

        new_chunk = self._make_chunk(page=2, text="new data")
        store.replace_all([new_chunk], [[0.3, 0.2, 0.1]])

        results = store.search([0.3, 0.2, 0.1], k=10)
        ids = [r.chunk.id for r in results]
        assert old_chunk.id not in ids
        assert new_chunk.id in ids


# ---------------------------------------------------------------------------
# retriever.py
# ---------------------------------------------------------------------------

class TestRetriever:
    def _make_mock_embedder(self, monkeypatch, embedding):
        from backend.embedder import Embedder
        embedder = Embedder()
        monkeypatch.setattr(embedder, "embed", lambda texts: [embedding for _ in texts])
        monkeypatch.setattr("backend.embedder.time.sleep", lambda s: None)
        return embedder

    def _make_mock_store(self, scored_chunks=None, raise_empty=False):
        from backend.vector_store import VectorStore
        store = VectorStore.__new__(VectorStore)

        class MockBackend:
            def search(self, query_embedding, k=5):
                if raise_empty:
                    raise EmptyKnowledgeBaseError("empty")
                return scored_chunks or []

        store._backend = MockBackend()
        return store

    def test_low_confidence_when_all_scores_below_threshold(self, monkeypatch):
        from backend.retriever import Retriever
        embedding = [0.1, 0.2, 0.3]
        embedder = self._make_mock_embedder(monkeypatch, embedding)

        chunk = Chunk(id="c1", text="text", page_number=1, char_offset=0)
        low_scored = [ScoredChunk(chunk=chunk, score=0.1)]
        store = self._make_mock_store(scored_chunks=low_scored)

        retriever = Retriever(embedder=embedder, vector_store=store)
        result = retriever.retrieve("what is diversification?")
        assert result.low_confidence is True

    def test_not_low_confidence_when_score_above_threshold(self, monkeypatch):
        from backend.retriever import Retriever
        embedding = [0.1, 0.2, 0.3]
        embedder = self._make_mock_embedder(monkeypatch, embedding)

        chunk = Chunk(id="c1", text="text", page_number=1, char_offset=0)
        high_scored = [ScoredChunk(chunk=chunk, score=0.8)]
        store = self._make_mock_store(scored_chunks=high_scored)

        retriever = Retriever(embedder=embedder, vector_store=store)
        result = retriever.retrieve("what is diversification?")
        assert result.low_confidence is False

    def test_propagates_empty_knowledge_base_error(self, monkeypatch):
        from backend.retriever import Retriever
        embedding = [0.1, 0.2, 0.3]
        embedder = self._make_mock_embedder(monkeypatch, embedding)
        store = self._make_mock_store(raise_empty=True)

        retriever = Retriever(embedder=embedder, vector_store=store)
        with pytest.raises(EmptyKnowledgeBaseError):
            retriever.retrieve("test query")


# ---------------------------------------------------------------------------
# response_generator.py
# ---------------------------------------------------------------------------

class TestResponseGenerator:
    def _make_chunks(self, pages=(1, 2, 3)):
        return [
            ScoredChunk(
                chunk=Chunk(id=str(uuid.uuid4()), text=f"text from page {p}", page_number=p, char_offset=0),
                score=0.9,
            )
            for p in pages
        ]

    def test_prompt_contains_query_and_chunk_texts(self):
        from backend.response_generator import _build_prompt
        chunks = self._make_chunks(pages=(1, 2))
        prompt = _build_prompt("what is diversification?", chunks)
        assert "what is diversification?" in prompt
        assert "text from page 1" in prompt
        assert "text from page 2" in prompt

    def test_prompt_contains_grounding_instruction(self):
        from backend.response_generator import _build_prompt
        chunks = self._make_chunks(pages=(1,))
        prompt = _build_prompt("test query", chunks)
        # The grounding instruction should tell the LLM to answer only from context
        assert "context" in prompt.lower() or "only" in prompt.lower()

    def test_citations_drawn_from_chunk_page_numbers(self):
        from backend.response_generator import _extract_citations
        chunks = self._make_chunks(pages=(3, 7, 3))  # page 3 appears twice
        citations = _extract_citations(chunks)
        assert set(citations) == {3, 7}
        assert citations == sorted(citations)

    def test_raises_llm_unavailable_after_3_failures(self, monkeypatch):
        from backend.response_generator import ResponseGenerator
        gen = ResponseGenerator()
        call_count = 0

        def failing_call(prompt, model):
            nonlocal call_count
            call_count += 1
            raise RuntimeError("LLM down")

        monkeypatch.setattr(gen, "_call_llm", failing_call)
        monkeypatch.setattr("backend.response_generator.time.sleep", lambda s: None)

        chunks = self._make_chunks(pages=(1,))
        with pytest.raises(LLMUnavailableError):
            gen.generate("test query", chunks)

        assert call_count == 3

    def test_retries_on_transient_llm_failure(self, monkeypatch):
        from backend.response_generator import ResponseGenerator
        gen = ResponseGenerator()
        call_count = 0

        def flaky_call(prompt, model):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RuntimeError("transient")
            return "The answer is diversification."

        monkeypatch.setattr(gen, "_call_llm", flaky_call)
        monkeypatch.setattr("backend.response_generator.time.sleep", lambda s: None)

        chunks = self._make_chunks(pages=(1,))
        result = gen.generate("test query", chunks)
        assert result.answer == "The answer is diversification."
        assert call_count == 2

    def test_low_confidence_propagated(self, monkeypatch):
        from backend.response_generator import ResponseGenerator
        gen = ResponseGenerator()
        monkeypatch.setattr(gen, "_call_llm", lambda p, m: "answer")

        chunks = self._make_chunks(pages=(1,))
        result = gen.generate("query", chunks, low_confidence=True)
        assert result.low_confidence is True

    def test_citations_in_generated_response(self, monkeypatch):
        from backend.response_generator import ResponseGenerator
        gen = ResponseGenerator()
        monkeypatch.setattr(gen, "_call_llm", lambda p, m: "answer")

        chunks = self._make_chunks(pages=(4, 7))
        result = gen.generate("query", chunks)
        assert set(result.citations) == {4, 7}
