import uuid
import tiktoken

from backend.exceptions import EmptyContentError
from backend.models import Chunk, PageText


class Chunker:
    def __init__(self, max_tokens: int = 512, overlap_tokens: int = 50):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self._enc = tiktoken.get_encoding("cl100k_base")

    def chunk(self, pages: list[PageText]) -> list[Chunk]:
        """
        Returns Chunk list with id, text, page_number, char_offset.
        Raises EmptyContentError if pages contain no text.
        """
        # Build full text and a char-offset-to-page mapping
        full_text = ""
        # List of (start_char, page_number) boundaries
        page_boundaries: list[tuple[int, int]] = []
        for page in pages:
            page_boundaries.append((len(full_text), page.page_number))
            full_text += page.text

        if not full_text.strip():
            raise EmptyContentError("No text content available to chunk.")

        # Encode the full text into tokens, keeping byte offsets
        # encode_ordinary returns token ids; we need char offsets per token
        tokens = self._enc.encode(full_text)

        if not tokens:
            raise EmptyContentError("No text content available to chunk.")

        # Build a mapping from token index → char offset in full_text
        # We decode each token individually to find its character length
        token_char_lengths = [len(self._enc.decode([t])) for t in tokens]
        token_char_offsets: list[int] = []
        offset = 0
        for length in token_char_lengths:
            token_char_offsets.append(offset)
            offset += length

        # Build page lookup: given a char offset, return the page number
        def page_for_char(char_off: int) -> int:
            # page_boundaries is sorted by start_char ascending
            page_num = page_boundaries[0][1]
            for start_char, pnum in page_boundaries:
                if char_off >= start_char:
                    page_num = pnum
                else:
                    break
            return page_num

        chunks: list[Chunk] = []
        token_start = 0
        n_tokens = len(tokens)

        while token_start < n_tokens:
            token_end = min(token_start + self.max_tokens, n_tokens)

            chunk_tokens = tokens[token_start:token_end]
            chunk_text = self._enc.decode(chunk_tokens)
            char_offset = token_char_offsets[token_start]
            page_number = page_for_char(char_offset)

            chunks.append(Chunk(
                id=str(uuid.uuid4()),
                text=chunk_text,
                page_number=page_number,
                char_offset=char_offset,
            ))

            if token_end == n_tokens:
                break

            # Next chunk starts (max_tokens - overlap_tokens) ahead
            token_start = token_end - self.overlap_tokens

        return chunks
