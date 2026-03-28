class UnsupportedFileError(Exception):
    """Raised when the uploaded file is not a valid PDF."""


class NoExtractableTextError(Exception):
    """Raised when a PDF contains no extractable text (e.g., image-only)."""


class EmptyContentError(Exception):
    """Raised when the Chunker receives empty or whitespace-only content."""


class EmbeddingModelError(Exception):
    """Raised when the embedding model fails after exhausting all retries."""


class WriteError(Exception):
    """Raised when a Vector_Store write operation fails."""

    def __init__(self, chunk_id: str, message: str = ""):
        self.chunk_id = chunk_id
        super().__init__(message or f"Failed to persist chunk {chunk_id}.")


class EmptyKnowledgeBaseError(Exception):
    """Raised when a query is attempted against an empty Vector_Store."""


class LLMUnavailableError(Exception):
    """Raised when the LLM fails to respond after exhausting all retries."""
