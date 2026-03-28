import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { PDFUpload } from "./PDFUpload";

describe("PDFUpload", () => {
  const onIngestionSuccess = vi.fn();

  beforeEach(() => {
    onIngestionSuccess.mockClear();
    vi.restoreAllMocks();
  });

  it("renders file input with accept='.pdf'", () => {
    render(<PDFUpload onIngestionSuccess={onIngestionSuccess} />);
    const input = screen.getByLabelText(/upload investment pdf/i);
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute("accept", ".pdf");
    expect(input).toHaveAttribute("type", "file");
  });

  it("shows loading indicator while uploading", async () => {
    // fetch that never resolves
    vi.stubGlobal("fetch", () => new Promise(() => {}));
    render(<PDFUpload onIngestionSuccess={onIngestionSuccess} />);

    const input = screen.getByLabelText(/upload investment pdf/i);
    const file = new File(["dummy"], "test.pdf", { type: "application/pdf" });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/uploading and ingesting pdf/i)).toBeInTheDocument();
    });
  });

  it("shows success message after successful upload", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({}) } as Response)
    );
    render(<PDFUpload onIngestionSuccess={onIngestionSuccess} />);

    const input = screen.getByLabelText(/upload investment pdf/i);
    const file = new File(["dummy"], "test.pdf", { type: "application/pdf" });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/pdf ingested successfully/i)).toBeInTheDocument();
    });
    expect(onIngestionSuccess).toHaveBeenCalledOnce();
  });

  it("shows error message on failed upload", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({
        ok: false,
        status: 422,
        json: () => Promise.resolve({ detail: "The uploaded file is not a valid PDF." }),
      } as Response)
    );
    render(<PDFUpload onIngestionSuccess={onIngestionSuccess} />);

    const input = screen.getByLabelText(/upload investment pdf/i);
    const file = new File(["dummy"], "test.pdf", { type: "application/pdf" });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/the uploaded file is not a valid pdf/i)).toBeInTheDocument();
    });
    expect(onIngestionSuccess).not.toHaveBeenCalled();
  });

  it("shows error message on network failure", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new Error("Network error")));
    render(<PDFUpload onIngestionSuccess={onIngestionSuccess} />);

    const input = screen.getByLabelText(/upload investment pdf/i);
    const file = new File(["dummy"], "test.pdf", { type: "application/pdf" });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });
  });
});
