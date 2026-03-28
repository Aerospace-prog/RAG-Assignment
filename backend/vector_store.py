"""
VectorStore: ChromaDB (local) and Firebase (cloud) backends.
Selected via VECTOR_STORE_BACKEND env var: 'chroma' (default) or 'firebase'.
"""

import math
import os
from typing import Optional

from backend.exceptions import EmptyKnowledgeBaseError, WriteError
from backend.models import Chunk, ScoredChunk


# ---------------------------------------------------------------------------
# Cosine similarity helper
# ---------------------------------------------------------------------------

def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


# ---------------------------------------------------------------------------
# ChromaDB backend
# ---------------------------------------------------------------------------

class _ChromaBackend:
    _COLLECTION_NAME = "investment_knowledge"

    def __init__(self) -> None:
        import chromadb  # type: ignore

        self._client = chromadb.PersistentClient(path="./chroma_db")
        self._collection = self._client.get_or_create_collection(
            name=self._COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    # ------------------------------------------------------------------
    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        try:
            self._collection.upsert(
                ids=[c.id for c in chunks],
                documents=[c.text for c in chunks],
                embeddings=embeddings,
                metadatas=[
                    {"page_number": c.page_number, "char_offset": c.char_offset}
                    for c in chunks
                ],
            )
        except Exception as exc:
            # Identify the first chunk id for the error message
            chunk_id = chunks[0].id if chunks else "unknown"
            raise WriteError(chunk_id) from exc

    # ------------------------------------------------------------------
    def search(self, query_embedding: list[float], k: int = 5) -> list[ScoredChunk]:
        count = self._collection.count()
        if count == 0:
            raise EmptyKnowledgeBaseError("No documents have been ingested yet.")

        n_results = min(k, count)
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        scored: list[ScoredChunk] = []
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for chunk_id, text, meta, distance in zip(ids, documents, metadatas, distances):
            # ChromaDB returns cosine *distance* (0 = identical, 2 = opposite)
            score = 1.0 - distance
            chunk = Chunk(
                id=chunk_id,
                text=text,
                page_number=meta["page_number"],
                char_offset=meta["char_offset"],
            )
            scored.append(ScoredChunk(chunk=chunk, score=score))

        # Results from ChromaDB are already ordered by ascending distance
        # (i.e. descending similarity), but sort explicitly to be safe.
        scored.sort(key=lambda sc: sc.score, reverse=True)
        return scored

    # ------------------------------------------------------------------
    def replace_all(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        import chromadb  # type: ignore

        # Delete and recreate the collection to clear all data
        try:
            self._client.delete_collection(self._COLLECTION_NAME)
        except Exception:
            pass  # Collection may not exist yet

        self._collection = self._client.get_or_create_collection(
            name=self._COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        if chunks:
            self.upsert(chunks, embeddings)


# ---------------------------------------------------------------------------
# Firebase backend
# ---------------------------------------------------------------------------

class _FirebaseBackend:
    _COLLECTION_NAME = "knowledge_base"

    def __init__(self) -> None:
        import firebase_admin  # type: ignore
        from firebase_admin import credentials, firestore  # type: ignore

        if not firebase_admin._apps:
            firebase_admin.initialize_app()

        self._db = firestore.client()

    # ------------------------------------------------------------------
    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        from firebase_admin import firestore  # type: ignore

        col = self._db.collection(self._COLLECTION_NAME)
        for chunk, embedding in zip(chunks, embeddings):
            try:
                col.document(chunk.id).set(
                    {
                        "chunk_id": chunk.id,
                        "text": chunk.text,
                        "page_number": chunk.page_number,
                        "char_offset": chunk.char_offset,
                        "embedding": embedding,
                        "ingestion_id": os.environ.get("INGESTION_ID", ""),
                    }
                )
            except Exception as exc:
                raise WriteError(chunk.id) from exc

    # ------------------------------------------------------------------
    def search(self, query_embedding: list[float], k: int = 5) -> list[ScoredChunk]:
        col = self._db.collection(self._COLLECTION_NAME)
        docs = list(col.stream())

        if not docs:
            raise EmptyKnowledgeBaseError("No documents have been ingested yet.")

        scored: list[ScoredChunk] = []
        for doc in docs:
            data = doc.to_dict()
            embedding: list[float] = data["embedding"]
            score = _cosine_similarity(query_embedding, embedding)
            chunk = Chunk(
                id=data["chunk_id"],
                text=data["text"],
                page_number=data["page_number"],
                char_offset=data["char_offset"],
            )
            scored.append(ScoredChunk(chunk=chunk, score=score))

        scored.sort(key=lambda sc: sc.score, reverse=True)
        return scored[:k]

    # ------------------------------------------------------------------
    def replace_all(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        from firebase_admin import firestore  # type: ignore

        col = self._db.collection(self._COLLECTION_NAME)
        # Delete all existing documents
        for doc in col.stream():
            doc.reference.delete()

        if chunks:
            self.upsert(chunks, embeddings)


# ---------------------------------------------------------------------------
# Public VectorStore facade
# ---------------------------------------------------------------------------

class VectorStore:
    """
    Facade that delegates to either ChromaDB or Firebase backend,
    selected via the VECTOR_STORE_BACKEND environment variable.
    """

    def __init__(self) -> None:
        backend_name = os.environ.get("VECTOR_STORE_BACKEND", "chroma").lower()
        if backend_name == "firebase":
            self._backend: _ChromaBackend | _FirebaseBackend = _FirebaseBackend()
        else:
            self._backend = _ChromaBackend()

    # ------------------------------------------------------------------
    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Persists all chunks. Raises WriteError on failure."""
        self._backend.upsert(chunks, embeddings)

    # ------------------------------------------------------------------
    def search(self, query_embedding: list[float], k: int = 5) -> list[ScoredChunk]:
        """
        Returns top-K chunks ranked by cosine similarity (descending).
        Raises EmptyKnowledgeBaseError if no chunks are stored.
        """
        return self._backend.search(query_embedding, k)

    # ------------------------------------------------------------------
    def replace_all(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Deletes all existing chunks/embeddings and writes new ones."""
        self._backend.replace_all(chunks, embeddings)
