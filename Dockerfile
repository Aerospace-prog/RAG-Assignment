# Multi-stage build for RAG Investment Analysis

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create necessary directories and set permissions (for Hugging Face Spaces)
RUN mkdir -p chroma_db uploads && chmod -R 777 chroma_db uploads

# Expose port (7860 for HF Spaces, 8000 for others)
EXPOSE 7860 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV EMBEDDING_MODEL=simple
ENV LLM_MODEL=simple
ENV HOST=0.0.0.0
ENV PORT=7860
ENV ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run the application
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
