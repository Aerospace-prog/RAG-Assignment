from __future__ import annotations

from typing import BinaryIO

import pypdf

from backend.exceptions import NoExtractableTextError, UnsupportedFileError
from backend.models import PageText


class PDFIngester:
    def ingest(self, file: BinaryIO) -> list[PageText]:
        """
        Returns a list of PageText (page_number, text) for each page.
        Raises UnsupportedFileError if not a valid PDF.
        Raises NoExtractableTextError if all pages yield empty text.
        """
        try:
            reader = pypdf.PdfReader(file)
        except Exception as exc:
            raise UnsupportedFileError(
                "The uploaded file is not a valid PDF."
            ) from exc

        pages: list[PageText] = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(PageText(page_number=i, text=text))

        if pages and all(not p.text.strip() for p in pages):
            raise NoExtractableTextError(
                "No text could be extracted from the PDF (possibly image-only)."
            )

        return pages
