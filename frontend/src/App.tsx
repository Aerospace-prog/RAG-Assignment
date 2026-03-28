import { useState } from "react";
import { PDFUpload } from "./components/PDFUpload";
import { QueryPanel } from "./components/QueryPanel";
import "./App.css";

function App() {
  const [ingested, setIngested] = useState(false);

  return (
    <div className="app-container">
      <div className="app-header">
        <h1 className="app-title">📚 RAG Investment Analysis</h1>
        <p className="app-subtitle">
          Upload documents and get AI-powered answers with source citations
        </p>
      </div>

      <div className="app-content">
        <div className="section">
          <div className="section-header">
            <div className="section-icon">📄</div>
            <div>
              <h2 className="section-title">Step 1: Upload Document</h2>
              <p className="section-description">
                Upload a PDF to analyze and query
              </p>
            </div>
          </div>
          <PDFUpload onIngestionSuccess={() => setIngested(true)} />
        </div>

        <div className="divider" />

        <div className="section">
          <div className="section-header">
            <div className="section-icon">💬</div>
            <div>
              <h2 className="section-title">Step 2: Ask Questions</h2>
              <p className="section-description">
                {ingested
                  ? "Your document is ready! Ask anything about its content"
                  : "Upload a document first to enable queries"}
              </p>
            </div>
          </div>
          <QueryPanel enabled={ingested} />
        </div>
      </div>
    </div>
  );
}

export default App;
