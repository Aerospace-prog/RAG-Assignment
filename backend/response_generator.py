import os
import time

from backend.exceptions import LLMUnavailableError
from backend.models import GeneratedResponse, ScoredChunk

_RETRY_DELAYS = [1, 2, 4]  # seconds before each retry attempt

_SYSTEM_INSTRUCTION = (
    "You are an investment analysis assistant. Answer the question based ONLY on the "
    "provided context.\nIf the context does not contain sufficient information, say so explicitly."
)


def _build_prompt(query: str, chunks: list[ScoredChunk]) -> str:
    context_lines = "\n".join(
        f"[Page {sc.chunk.page_number}]: {sc.chunk.text}" for sc in chunks
    )
    return (
        f"{_SYSTEM_INSTRUCTION}\n\n"
        f"Context:\n{context_lines}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )


def _extract_citations(chunks: list[ScoredChunk]) -> list[int]:
    return sorted({sc.chunk.page_number for sc in chunks})


class ResponseGenerator:
    """Builds a grounded prompt from retrieved chunks and calls the LLM."""

    def generate(
        self,
        query: str,
        chunks: list[ScoredChunk],
        low_confidence: bool = False,
    ) -> GeneratedResponse:
        """Returns GeneratedResponse with answer text and source page citations.

        Retries the LLM call up to 3 times with exponential backoff (1 s, 2 s, 4 s).
        Raises LLMUnavailableError after exhausting retries.
        The low_confidence flag is propagated directly to GeneratedResponse.
        """
        prompt = _build_prompt(query, chunks)
        citations = _extract_citations(chunks)
        model = os.environ.get("LLM_MODEL", "simple")

        last_exc: Exception | None = None

        for attempt in range(3):
            if attempt > 0:
                time.sleep(_RETRY_DELAYS[attempt - 1])
            try:
                if model == "simple":
                    answer = self._call_llm_simple(prompt)
                elif model == "huggingface":
                    answer = self._call_llm_huggingface(prompt)
                else:
                    answer = self._call_llm_openai(prompt, model)
                return GeneratedResponse(
                    answer=answer,
                    citations=citations,
                    low_confidence=low_confidence,
                )
            except Exception as exc:
                last_exc = exc

        raise LLMUnavailableError(
            f"LLM failed after 3 attempts: {last_exc}"
        ) from last_exc

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _call_llm_simple(self, prompt: str) -> str:
        """Use simple rule-based LLM (no API needed)."""
        from backend.simple_llm import SimpleLLM
        
        llm = SimpleLLM()
        return llm.generate(prompt)

    def _call_llm_openai(self, prompt: str, model: str) -> str:
        import openai

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""

    def _call_llm_huggingface(self, prompt: str) -> str:
        """Use Hugging Face Inference API with a free model."""
        import requests
        
        # Use a free instruction-following model
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        # Get API token from env (optional - free tier works without it but has rate limits)
        headers = {}
        hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "return_full_text": False,
                },
                "options": {"wait_for_model": True},
            },
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated text
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").strip()
        elif isinstance(result, dict):
            return result.get("generated_text", "").strip()
        
        return "Unable to generate response."
