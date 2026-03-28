from dataclasses import dataclass, field


@dataclass
class PageText:
    page_number: int  # 1-indexed
    text: str


@dataclass
class Chunk:
    id: str           # UUID
    text: str
    page_number: int
    char_offset: int  # character offset within the full extracted text


@dataclass
class ScoredChunk:
    chunk: Chunk
    score: float      # cosine similarity in [0, 1]


@dataclass
class RetrievalResult:
    scored_chunks: list[ScoredChunk]
    low_confidence: bool  # True when max(score) < 0.3


@dataclass
class GeneratedResponse:
    answer: str
    citations: list[int]  # page numbers that contributed to the answer
    low_confidence: bool  # propagated from RetrievalResult


@dataclass
class StoredRecord:
    chunk: Chunk
    embedding: list[float]
