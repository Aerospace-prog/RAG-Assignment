import os
import time

from backend.exceptions import EmbeddingModelError

_RETRY_DELAYS = [1, 2, 4]  # seconds before each retry attempt


class Embedder:
    """Generates vector embeddings for text strings.

    Selects the embedding backend based on the EMBEDDING_MODEL env var:
      - "simple" (default): Fast TF-IDF based embeddings (no API, completely free)
      - "huggingface": Free Hugging Face API (requires internet, may have rate limits)
      - "openai": OpenAI text-embedding-3-small (requires API key)
      - "local": sentence-transformers/all-MiniLM-L6-v2 (requires installation)
    """

    def __init__(self):
        self._simple_embedder = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Returns one embedding vector per input text.

        Retries up to 3 times on transient errors with exponential backoff
        (1 s, 2 s, 4 s). Raises EmbeddingModelError after exhausting retries.
        """
        model = os.environ.get("EMBEDDING_MODEL", "simple")
        last_exc: Exception | None = None

        for attempt in range(3):
            if attempt > 0:
                time.sleep(_RETRY_DELAYS[attempt - 1])
            try:
                if model == "simple":
                    return self._embed_simple(texts)
                elif model == "local":
                    return self._embed_local(texts)
                elif model == "openai":
                    return self._embed_openai(texts)
                else:
                    return self._embed_huggingface(texts)
            except Exception as exc:
                last_exc = exc

        raise EmbeddingModelError(
            f"Embedding model failed after 3 attempts: {last_exc}"
        ) from last_exc

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _embed_simple(self, texts: list[str]) -> list[list[float]]:
        """Use simple TF-IDF based embeddings (no API needed)."""
        from backend.simple_embedder import SimpleEmbedder
        
        if self._simple_embedder is None:
            self._simple_embedder = SimpleEmbedder(dimension=384)
        
        return self._simple_embedder.embed(texts)

    def _embed_openai(self, texts: list[str]) -> list[list[float]]:
        import openai

        client = openai.OpenAI()
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )
        # Results are returned in the same order as the input
        return [item.embedding for item in response.data]

    def _embed_local(self, texts: list[str]) -> list[list[float]]:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model.encode(texts).tolist()

    def _embed_huggingface(self, texts: list[str]) -> list[list[float]]:
        """Use Hugging Face Inference API (free tier)."""
        import requests
        
        # Use a free embedding model from Hugging Face
        API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        
        # Get API token from env (optional - free tier works without it but has rate limits)
        headers = {}
        hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"
        
        embeddings = []
        for text in texts:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": text, "options": {"wait_for_model": True}},
                timeout=30,
            )
            response.raise_for_status()
            # The API returns the embedding directly
            embedding = response.json()
            if isinstance(embedding, list) and isinstance(embedding[0], list):
                # Sometimes returns [[embedding]]
                embedding = embedding[0]
            embeddings.append(embedding)
        
        return embeddings
