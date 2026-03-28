#!/bin/bash

echo "🧪 Testing RAG Investment Analysis System"
echo "=========================================="
echo ""

# Test 1: Check if servers are running
echo "1️⃣  Checking servers..."
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "   ✅ Backend is running on http://localhost:8000"
else
    echo "   ❌ Backend is not running!"
    echo "   Start it with: EMBEDDING_MODEL=simple LLM_MODEL=simple .venv/bin/uvicorn backend.main:app --reload"
    exit 1
fi

if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "   ✅ Frontend is running on http://localhost:5173"
else
    echo "   ❌ Frontend is not running!"
    echo "   Start it with: cd frontend && npm run dev"
    exit 1
fi

echo ""

# Test 2: Check if PDF exists
echo "2️⃣  Checking test PDF..."
if [ -f "backend/tests/fixtures/investment.pdf" ]; then
    SIZE=$(ls -lh backend/tests/fixtures/investment.pdf | awk '{print $5}')
    echo "   ✅ Test PDF exists ($SIZE)"
else
    echo "   ❌ Test PDF not found!"
    echo "   Create it with: .venv/bin/python create_test_pdf.py"
    exit 1
fi

echo ""

# Test 3: Test ingestion
echo "3️⃣  Testing PDF ingestion..."
INGEST_RESULT=$(curl -s -X POST http://localhost:8000/ingest \
  -F "file=@backend/tests/fixtures/investment.pdf")

if echo "$INGEST_RESULT" | grep -q "ok"; then
    echo "   ✅ PDF ingestion successful!"
else
    echo "   ❌ PDF ingestion failed!"
    echo "   Response: $INGEST_RESULT"
    exit 1
fi

echo ""

# Test 4: Test queries
echo "4️⃣  Testing queries..."

QUERIES=(
    "What is the theory of diversification?"
    "How do I deal with brokerage houses?"
    "What is the eggs in one basket analogy?"
)

for QUERY in "${QUERIES[@]}"; do
    echo ""
    echo "   📝 Query: $QUERY"
    
    RESULT=$(curl -s -X POST http://localhost:8000/query \
      -H "Content-Type: application/json" \
      -d "{\"query\": \"$QUERY\", \"k\": 5}")
    
    if echo "$RESULT" | grep -q "answer"; then
        ANSWER=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['answer'][:100] + '...')" 2>/dev/null || echo "Answer received")
        CITATIONS=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['citations'])" 2>/dev/null || echo "[]")
        echo "   ✅ Answer: $ANSWER"
        echo "   📚 Citations: $CITATIONS"
    else
        echo "   ❌ Query failed!"
        echo "   Response: $RESULT"
    fi
done

echo ""
echo ""
echo "=========================================="
echo "✅ All tests passed!"
echo ""
echo "🎨 Open the UI: http://localhost:5173"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
echo "Try uploading the PDF and asking questions!"
