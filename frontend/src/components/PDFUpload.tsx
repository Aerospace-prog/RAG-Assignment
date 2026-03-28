import React, { useState, useRef } from "react";
import "./PDFUpload.css";

interface PDFUploadProps {
  onIngestionSuccess: () => void;
}

type UploadState = "idle" | "loading" | "success" | "error";

export function PDFUpload({ onIngestionSuccess }: PDFUploadProps) {
  const [state, setState] = useState<UploadState>("idle");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [fileName, setFileName] = useState<string>("");
  const [fileSize, setFileSize] = useState<string>("");
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  const handleFile = async (file: File) => {
    if (!file.type.includes("pdf")) {
      setErrorMessage("Please select a PDF file");
      setState("error");
      return;
    }

    setFileName(file.name);
    setFileSize(formatFileSize(file.size));
    setState("loading");
    setErrorMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/ingest", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        const msg = data?.detail ?? `Upload failed with status ${res.status}.`;
        setErrorMessage(msg);
        setState("error");
        return;
      }

      setState("success");
      onIngestionSuccess();
    } catch (err) {
      setErrorMessage(
        err instanceof Error ? err.message : "An unexpected error occurred."
      );
      setState("error");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  const handleClick = () => {
    if (state !== "loading") {
      inputRef.current?.click();
    }
  };

  const handleReset = () => {
    setState("idle");
    setFileName("");
    setFileSize("");
    setErrorMessage("");
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="upload-container">
      {state === "idle" && (
        <div
          className={`upload-area ${isDragging ? "dragging" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <div className="upload-icon-large">📄</div>
          <div className="upload-text">
            <div className="upload-text-primary">
              Drop your PDF here or click to browse
            </div>
            <div className="upload-text-secondary">
              Supports PDF files up to 50MB
            </div>
          </div>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            className="upload-input"
          />
        </div>
      )}

      {(state === "loading" || state === "success") && fileName && (
        <div className="file-info">
          <div className="file-icon">📄</div>
          <div className="file-details">
            <div className="file-name">{fileName}</div>
            <div className="file-size">{fileSize}</div>
          </div>
          {state === "success" && (
            <div className="file-actions">
              <button
                className="btn-icon"
                onClick={handleReset}
                title="Upload another file"
              >
                🔄
              </button>
            </div>
          )}
        </div>
      )}

      {state === "loading" && (
        <div className="status-message status-loading">
          <div className="status-icon">
            <div className="spinner" />
          </div>
          <div className="status-content">
            <div className="status-title">Processing your document...</div>
            <div className="status-description">
              Extracting text, creating embeddings, and indexing content. This may take a moment.
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: "100%" }} />
            </div>
          </div>
        </div>
      )}

      {state === "success" && (
        <div className="status-message status-success">
          <div className="status-icon">✓</div>
          <div className="status-content">
            <div className="status-title">Document processed successfully!</div>
            <div className="status-description">
              Your PDF has been indexed and is ready for questions. You can now ask anything about the content below.
            </div>
          </div>
        </div>
      )}

      {state === "error" && (
        <div className="status-message status-error">
          <div className="status-icon">✕</div>
          <div className="status-content">
            <div className="status-title">Upload failed</div>
            <div className="status-description">{errorMessage}</div>
          </div>
        </div>
      )}
    </div>
  );
}
