import React, { useState } from "react";
import "./QueryPanel.css";

interface QueryPanelProps {
  enabled: boolean;
}

interface QueryResponse {
  answer: string;
  citations: number[];
  low_confidence: boolean;
}

const QUICK_QUESTIONS = [
  "What is the theory of diversification?",
  "How do I deal with brokerage houses?",
  "What is the eggs in one basket analogy?",
  "How do I become an intelligent investor?",
];

export function QueryPanel({ enabled }: QueryPanelProps) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string>("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    await executeQuery(query.trim());
  }

  async function executeQuery(questionText: string) {
    setLoading(true);
    setResponse(null);
    setError("");
    setQuery(questionText);

    try {
      const res = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: questionText }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data?.detail ?? `Request failed with status ${res.status}.`);
        return;
      }

      const data: QueryResponse = await res.json();
      setResponse(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unexpected error occurred."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleQuickQuestion(question: string) {
    executeQuery(question);
  }

  function handleCopyAnswer() {
    if (response) {
      navigator.clipboard.writeText(response.answer);
    }
  }

  function handleNewQuestion() {
    setResponse(null);
    setError("");
    setQuery("");
  }

  return (
    <div className="query-container">
      <form onSubmit={handleSubmit} className="query-form">
        <div className="query-input-group">
          <div className="query-input-wrapper">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={!enabled || loading}
              placeholder={
                enabled
                  ? "Ask anything about your document..."
                  : "Upload a PDF first to enable queries"
              }
              className="query-input"
            />
            <span className="input-icon">💬</span>
          </div>
          <button
            type="submit"
            disabled={!enabled || loading || !query.trim()}
            className="query-button"
          >
            {loading ? (
              <>
                <span>Thinking...</span>
                <span>🤔</span>
              </>
            ) : (
              <>
                <span>Ask</span>
                <span>✨</span>
              </>
            )}
          </button>
        </div>

        {enabled && !loading && !response && (
          <div className="quick-questions">
            <div className="quick-question-label">💡 Try these questions:</div>
            {QUICK_QUESTIONS.map((q, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleQuickQuestion(q)}
                className="quick-question-btn"
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        )}
      </form>

      {loading && (
        <div className="query-loading">
          <div className="loading-spinner" />
          <div className="loading-text">
            <div className="loading-title">Analyzing your question...</div>
            <div className="loading-description">
              Searching through the document and generating an answer
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="query-error">
          <div className="error-icon">⚠️</div>
          <div className="error-content">
            <div className="error-title">Something went wrong</div>
            <div className="error-message">{error}</div>
          </div>
        </div>
      )}

      {response && (
        <div className="query-response">
          {response.low_confidence && (
            <div className="low-confidence-warning">
              <div className="warning-icon">⚠️</div>
              <div className="warning-content">
                <div className="warning-title">Low Confidence Result</div>
                <div className="warning-description">
                  The retrieved passages may not be closely related to your question.
                  The answer might be less accurate. Try rephrasing your question.
                </div>
              </div>
            </div>
          )}

          <div className="answer-card">
            <div className="answer-header">
              <div className="answer-icon">💡</div>
              <div className="answer-label">Answer</div>
            </div>

            <div className="answer-text">{response.answer}</div>

            {response.citations.length > 0 && (
              <div className="citations">
                <div className="citations-label">
                  <span>📚</span>
                  <span>Sources:</span>
                </div>
                {response.citations.map((page, idx) => (
                  <div key={idx} className="citation-badge">
                    <span>Page {page}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="action-buttons">
            <button
              type="button"
              onClick={handleCopyAnswer}
              className="btn-secondary"
            >
              <span>📋</span>
              <span>Copy Answer</span>
            </button>
            <button
              type="button"
              onClick={handleNewQuestion}
              className="btn-secondary"
            >
              <span>🔄</span>
              <span>Ask Another Question</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
