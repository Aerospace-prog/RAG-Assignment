import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryPanel } from "./QueryPanel";

describe("QueryPanel", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("renders query text input", () => {
    render(<QueryPanel enabled={true} />);
    const input = screen.getByLabelText(/ask a question/i);
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute("type", "text");
  });

  it("disables input and button when not enabled", () => {
    render(<QueryPanel enabled={false} />);
    const input = screen.getByLabelText(/ask a question/i);
    const button = screen.getByRole("button", { name: /ask/i });
    expect(input).toBeDisabled();
    expect(button).toBeDisabled();
  });

  it("shows loading indicator while awaiting response", async () => {
    vi.stubGlobal("fetch", () => new Promise(() => {}));
    render(<QueryPanel enabled={true} />);

    const input = screen.getByLabelText(/ask a question/i);
    fireEvent.change(input, { target: { value: "what is diversification?" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText(/generating answer/i)).toBeInTheDocument();
    });
  });

  it("displays answer and citations on success", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            answer: "Diversification reduces risk.",
            citations: [3, 7],
            low_confidence: false,
          }),
      } as Response)
    );
    render(<QueryPanel enabled={true} />);

    const input = screen.getByLabelText(/ask a question/i);
    fireEvent.change(input, { target: { value: "what is diversification?" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText(/diversification reduces risk/i)).toBeInTheDocument();
    });
    expect(screen.getByText(/3, 7/)).toBeInTheDocument();
  });

  it("shows low-confidence warning when low_confidence is true", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            answer: "Some answer.",
            citations: [1],
            low_confidence: true,
          }),
      } as Response)
    );
    render(<QueryPanel enabled={true} />);

    const input = screen.getByLabelText(/ask a question/i);
    fireEvent.change(input, { target: { value: "obscure question" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText(/low confidence/i)).toBeInTheDocument();
    });
  });

  it("displays error message on API failure", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve({
        ok: false,
        status: 400,
        json: () =>
          Promise.resolve({ detail: "No documents have been ingested yet." }),
      } as Response)
    );
    render(<QueryPanel enabled={true} />);

    const input = screen.getByLabelText(/ask a question/i);
    fireEvent.change(input, { target: { value: "test query" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText(/no documents have been ingested yet/i)).toBeInTheDocument();
    });
  });

  it("displays error message on network failure", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new Error("Failed to fetch")));
    render(<QueryPanel enabled={true} />);

    const input = screen.getByLabelText(/ask a question/i);
    fireEvent.change(input, { target: { value: "test query" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
    });
  });

  it("allows submitting a new query without page reload", async () => {
    let callCount = 0;
    vi.stubGlobal("fetch", () => {
      callCount++;
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            answer: `Answer ${callCount}`,
            citations: [],
            low_confidence: false,
          }),
      } as Response);
    });
    render(<QueryPanel enabled={true} />);

    const input = screen.getByLabelText(/ask a question/i);

    // First query
    fireEvent.change(input, { target: { value: "first question" } });
    fireEvent.submit(input.closest("form")!);
    await waitFor(() => expect(screen.getByText(/answer 1/i)).toBeInTheDocument());

    // Second query without reload
    fireEvent.change(input, { target: { value: "second question" } });
    fireEvent.submit(input.closest("form")!);
    await waitFor(() => expect(screen.getByText(/answer 2/i)).toBeInTheDocument());

    expect(callCount).toBe(2);
  });
});
