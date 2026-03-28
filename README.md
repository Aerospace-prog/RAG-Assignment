---
title: RAG Investment Analysis
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
pinned: false
---

# 🤖 RAG Investment Analysis

A Retrieval-Augmented Generation (RAG) system for analyzing investment textbooks. Upload a PDF, ask questions, and get AI-powered answers with source citations.

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square)
![Tech Stack](https://img.shields.io/badge/AI-Free_Models-412991?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Vector_DB-ChromaDB-FF6F00?style=flat-square)
![Deployment](https://img.shields.io/badge/Deploy-Docker-2496ED?style=flat-square)

---

## ✨ Features

- 📄 **PDF Upload**: Ingest investment textbooks and documents with drag & drop
- 🔍 **Semantic Search**: Find relevant passages using vector embeddings
- 💬 **AI Answers**: Get natural language answers (free or paid models)
- 📚 **Source Citations**: Every answer includes page number references
- ⚠️ **Confidence Indicators**: Know when the AI is uncertain
- 🎨 **Modern UI**: Clean, responsive interface with smooth animations
- 🆓 **100% Free Option**: Works completely offline with no API costs
- 🐳 **Docker Ready**: One-command deployment with Docker Compose

---

## 🚀 Quick Start

### Option 1: Docker (Recommended for Production)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Build and run
docker-compose up --build

# 3. Open browser
# Navigate to http://localhost:8000
```

That's it! The application is now running with frontend and backend combined.

### Option 2: Development Mode

#### Prerequisites

- Python 3.12+ with pip
- Node.js 18+ with npm
- (Optional) OpenAI API key for better quality

#### Setup

```bash
# 1. Install backend dependencies
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt

# 2. Install frontend dependencies
cd frontend
npm install
cd ..

# 3. Configure models (optional)
export EMBEDDING_MODEL=simple  # Free, offline (default)
export LLM_MODEL=simple        # Free, offline (default)

# Or use OpenAI for better quality (requires API key)
# export EMBEDDING_MODEL=openai
# export LLM_MODEL=openai
# export OPENAI_API_KEY=sk-your-key-here
```

#### Start Servers

```bash
# Use the start script
chmod +x start.sh
./start.sh

# Or manually:
# Terminal 1 - Backend
.venv/bin/uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

#### Open Browser

Navigate to **http://localhost:5173** (dev) or **http://localhost:8000** (production)

---

## 📖 Usage

1. **Upload PDF**: Click "Choose Investment PDF" and select your document
2. **Wait for Processing**: The system will chunk, embed, and index the content
3. **Ask Questions**: Type your question in natural language
4. **Get Answers**: Receive AI-generated answers with page citations

### Example Questions

- "What is diversification?"
- "How do I choose a brokerage house?"
- "What is the theory of asset allocation?"
- "How should I balance risk and return?"

---


## 🚢 Deployment

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guide covering:

- Docker deployment (recommended)
- Cloud platforms (Railway, Render, Heroku, AWS, DigitalOcean)
- SSL/HTTPS setup with Nginx
- Environment configuration
- Monitoring and health checks
- Backup strategies
- Performance tuning
- Security best practices

### Quick Production Build

```bash
# Build frontend
./build.sh

# Run with Docker
docker-compose up --build -d

# Or run manually
export ENVIRONMENT=production
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "environment": "production",
  "embedding_model": "simple",
  "llm_model": "simple"
}
```

---

## 🧪 Testing

```bash
# Backend unit tests (40+ tests)
.venv/bin/pytest -m "not e2e" -v

# Frontend tests (13 tests)
cd frontend && npm test

# End-to-end test (requires PDF + API key)
.venv/bin/pytest -m e2e -v
```

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│  ChromaDB   │
│  Frontend   │      │   Backend    │      │ Vector Store│
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  OpenAI API  │
                     │ (Embeddings  │
                     │  + GPT-4)    │
                     └──────────────┘
```

### Pipeline Flow

**Ingestion:**
```
PDF → Text Extraction → Chunking → Embedding → Vector Storage
```

**Query:**
```
Question → Embedding → Similarity Search → Context Retrieval → LLM Generation → Answer + Citations
```

---

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI routes
│   ├── ingester.py          # PDF text extraction
│   ├── chunker.py           # Text chunking
│   ├── embedder.py          # Vector embeddings
│   ├── vector_store.py      # ChromaDB interface
│   ├── retriever.py         # Semantic search
│   ├── response_generator.py # LLM response generation
│   ├── models.py            # Data models
│   ├── exceptions.py        # Custom exceptions
│   └── tests/               # Unit & E2E tests
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main app component
│   │   ├── components/
│   │   │   ├── PDFUpload.tsx    # Upload component
│   │   │   └── QueryPanel.tsx   # Query component
│   │   └── *.css            # Styling
│   └── package.json
├── TESTING_GUIDE.md         # Detailed testing instructions
└── README.md                # This file
```

---

## 🎨 Tech Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic OpenAPI docs
- **pypdf**: PDF text extraction
- **tiktoken**: Token counting for chunking
- **Simple Models**: Free TF-IDF embeddings + rule-based LLM (default)
- **OpenAI API**: Optional paid embeddings + GPT models
- **ChromaDB**: Vector database for semantic search
- **pytest + Hypothesis**: Testing framework with property-based tests

### Frontend
- **React 18**: UI framework with hooks
- **TypeScript**: Type safety and better DX
- **Vite**: Lightning-fast build tool and dev server
- **Vitest**: Testing framework
- **CSS3**: Custom styling with CSS variables, gradients, and animations

### DevOps
- **Docker**: Containerization with multi-stage builds
- **Docker Compose**: Container orchestration
- **Uvicorn**: ASGI server for FastAPI
- **Nginx**: Reverse proxy for production (optional)

---

## 🔧 Configuration

### Model Options

The system supports multiple embedding and LLM backends:

| Model Type | Option | Cost | Quality | Speed |
|------------|--------|------|---------|-------|
| **Embedding** | `simple` | Free | Basic | Fast |
| | `openai` | Paid | Excellent | Fast |
| | `huggingface` | Free | Good | Medium |
| **LLM** | `simple` | Free | Basic | Fast |
| | `openai` | Paid | Excellent | Medium |
| | `huggingface` | Free | Good | Slow |

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Model Configuration (defaults to free)
EMBEDDING_MODEL=simple
LLM_MODEL=simple

# OpenAI (optional, for better quality)
OPENAI_API_KEY=sk-...

# Hugging Face (optional)
HUGGINGFACE_API_TOKEN=hf_...

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DEBUG=false

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Vector Store
VECTOR_STORE_BACKEND=chroma
CHROMA_DB_PATH=./chroma_db

# Limits
MAX_UPLOAD_SIZE=52428800  # 50MB
MAX_CHUNK_SIZE=512
CHUNK_OVERLAP=50
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete configuration guide.

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure you're in the workspace root
pwd  # Should show: /path/to/RAG ASSIGNMENT

# Use the venv's uvicorn
.venv/bin/uvicorn backend.main:app --reload
```

### Frontend shows network errors
```bash
# Check backend is running
curl http://localhost:8000/docs

# Check CORS is enabled (it should be by default)
```

### Tests fail
```bash
# Install all dependencies
.venv/bin/pip install -r backend/requirements.txt
cd frontend && npm install

# Run tests individually
.venv/bin/pytest -v
cd frontend && npm test
```

---

## 📊 Performance

- **Ingestion**: ~30-60 seconds for a 50-page PDF
- **Query**: ~2-5 seconds per question
- **Embedding Model**: 384 dimensions (text-embedding-3-small)
- **Chunk Size**: 512 tokens with 50-token overlap
- **Retrieval**: Top-5 most relevant chunks

---

## 💰 Cost Estimates

### Free Tier (Default)

Using `EMBEDDING_MODEL=simple` and `LLM_MODEL=simple`:
- **Ingestion**: $0 (completely free)
- **Query**: $0 (completely free)
- **Total**: $0 - Works 100% offline

### Paid Tier (Better Quality)

Using `EMBEDDING_MODEL=openai` and `LLM_MODEL=openai`:
- **Ingestion**: ~$0.01-0.05 per 50-page PDF
- **Query**: ~$0.001-0.01 per question
- **Total for testing**: Well within OpenAI's $5 free credits

---

## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing instructions
- [FINAL_SUMMARY.md](FINAL_SUMMARY.md) - Project summary
- `.kiro/specs/rag-investment-analysis/` - Spec-driven development docs

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

Built with:
- FastAPI and React for the application stack
- ChromaDB for vector storage
- OpenAI API (optional) for embeddings and LLM
- Free TF-IDF and rule-based models for offline operation
- Docker for containerization

---

**Made with ❤️ using RAG technology**

**Ready for production deployment! See [DEPLOYMENT.md](DEPLOYMENT.md) to get started.**
