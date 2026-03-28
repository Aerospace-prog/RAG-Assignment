#!/bin/bash

# RAG Investment Analysis - Quick Start Script

echo "🚀 Starting RAG Investment Analysis..."
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY is not set!"
    echo "   Set it with: export OPENAI_API_KEY=sk-your-key-here"
    echo "   Or use local embeddings: export EMBEDDING_MODEL=local"
    echo ""
fi

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Create it with: python3 -m venv .venv"
    echo "   Then install: .venv/bin/pip install -r backend/requirements.txt"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "   Install with: cd frontend && npm install"
    exit 1
fi

echo "✅ Environment checks passed"
echo ""

# Start backend in background
echo "🔧 Starting backend server on http://localhost:8000..."
.venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting frontend server on http://localhost:5173..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "   Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 3

echo ""
echo "✨ Both servers are running!"
echo ""
echo "📱 Open your browser to: http://localhost:5173"
echo "📚 API docs available at: http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   Or press Ctrl+C and run: pkill -f uvicorn && pkill -f vite"
echo ""

# Save PIDs to file for easy cleanup
echo "$BACKEND_PID" > .server_pids
echo "$FRONTEND_PID" >> .server_pids

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .server_pids; echo '✅ Servers stopped'; exit 0" INT

echo "Press Ctrl+C to stop all servers"
wait
