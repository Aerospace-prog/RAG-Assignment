#!/bin/bash
# Build script for RAG Investment Analysis

set -e

echo "🏗️  Building RAG Investment Analysis..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build complete!"
echo ""
echo "Frontend build available at: frontend/dist"
echo ""
echo "To run in production mode:"
echo "  1. Set environment variables (copy .env.example to .env)"
echo "  2. Run: uvicorn backend.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Or use Docker:"
echo "  docker-compose up --build"
