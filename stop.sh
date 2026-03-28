#!/bin/bash

# Stop all servers

echo "🛑 Stopping RAG Investment Analysis servers..."

if [ -f ".server_pids" ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null
            echo "   Stopped process $pid"
        fi
    done < .server_pids
    rm -f .server_pids
fi

# Fallback: kill by process name
pkill -f "uvicorn backend.main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "✅ All servers stopped"
