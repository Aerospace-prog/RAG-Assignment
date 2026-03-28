import io
import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from backend.config import settings
from backend.exceptions import (
    UnsupportedFileError,
    NoExtractableTextError,
    EmptyContentError,
    EmbeddingModelError,
    WriteError,
    EmptyKnowledgeBaseError,
    LLMUnavailableError,
)
from backend.ingester import PDFIngester
from backend.chunker import Chunker
from backend.embedder import Embedder
from backend.vector_store import VectorStore
from backend.retriever import Retriever
from backend.response_generator import ResponseGenerator

app = FastAPI(
    title="RAG Investment Analysis",
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.DEBUG else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup."""
    settings.validate()
    print(f"🚀 Starting RAG Investment Analysis in {settings.ENVIRONMENT} mode")
    print(f"📊 Embedding Model: {settings.EMBEDDING_MODEL}")
    print(f"🤖 LLM Model: {settings.LLM_MODEL}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 Shutting down RAG Investment Analysis")


class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 5


class QueryResponse(BaseModel):
    answer: str
    citations: list[int]
    low_confidence: bool


@app.post("/ingest", status_code=200)
async def ingest(file: UploadFile = File(...)):
    """Accept a multipart PDF upload and run the ingestion pipeline."""
    contents = await file.read()
    try:
        pages = PDFIngester().ingest(io.BytesIO(contents))
        chunks = Chunker().chunk(pages)
        embedder = Embedder()
        embeddings = embedder.embed([c.text for c in chunks])
        VectorStore().upsert(chunks, embeddings)
    except UnsupportedFileError:
        raise HTTPException(status_code=422, detail="The uploaded file is not a valid PDF.")
    except NoExtractableTextError:
        raise HTTPException(status_code=422, detail="No text could be extracted from the PDF (possibly image-only).")
    except EmptyContentError:
        raise HTTPException(status_code=422, detail="The document contains no text content to process.")
    except EmbeddingModelError:
        raise HTTPException(status_code=503, detail="The embedding model is unavailable after 3 retries.")
    except WriteError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to persist chunk {exc.chunk_id}.")
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Accept a natural language query and return an answer with citations."""
    try:
        embedder = Embedder()
        vector_store = VectorStore()
        retriever = Retriever(embedder=embedder, vector_store=vector_store)
        result = retriever.retrieve(request.query, k=request.k)
        response = ResponseGenerator().generate(
            request.query, result.scored_chunks, low_confidence=result.low_confidence
        )
    except EmptyKnowledgeBaseError:
        raise HTTPException(
            status_code=400,
            detail="No documents have been ingested yet. Please upload a PDF first.",
        )
    except EmbeddingModelError:
        raise HTTPException(
            status_code=503,
            detail="The embedding model is unavailable after 3 retries.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="The language model is unavailable after 3 retries.",
        )
    return QueryResponse(
        answer=response.answer,
        citations=response.citations,
        low_confidence=response.low_confidence,
    )


@app.delete("/knowledge-base", status_code=200)
async def clear_knowledge_base():
    """Clear all stored chunks and embeddings."""
    VectorStore().replace_all([], [])
    return {"status": "ok"}


@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "embedding_model": settings.EMBEDDING_MODEL,
        "llm_model": settings.LLM_MODEL,
    }


# Serve static frontend files (production only)
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists() and settings.is_production():
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    # Serve index.html for all other routes (SPA fallback)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes."""
        # If path starts with /api, /docs, /openapi.json, let FastAPI handle it
        if full_path.startswith(("api/", "docs", "openapi.json", "health")):
            raise HTTPException(status_code=404, detail="Not found")
        
        # Serve index.html for all other routes
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend not built")
