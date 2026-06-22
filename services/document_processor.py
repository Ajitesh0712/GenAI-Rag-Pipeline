from pathlib import Path
from pypdf import PdfReader
from docx import Document
import logging
import re

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Remove duplicate whitespace.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def extract_pdf(file_path: str):

    pages = []

    reader = PdfReader(file_path)

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        try:

            text = page.extract_text()

            text = clean_text(text)

            pages.append(
                {
                    "page": page_number,
                    "text": text
                }
            )

        except Exception as e:

            logger.error(
                f"Page {page_number}: {e}"
            )

    return pages

def extract_docx(file_path: str):

    document = Document(file_path)

    paragraphs = []

    for para in document.paragraphs:

        text = para.text.strip()

        if text:
            paragraphs.append(text)

    combined_text = "\n".join(paragraphs)

    return [
        {
            "page": 1,
            "text": clean_text(combined_text)
        }
    ]


def extract_txt(file_path: str):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

    except UnicodeDecodeError:

        with open(
            file_path,
            "r",
            encoding="latin-1"
        ) as f:

            text = f.read()

    return [
        {
            "page": 1,
            "text": clean_text(text)
        }
    ]

def extract_document(file_path: str):

    extension = (
        Path(file_path)
        .suffix
        .lower()
    )

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    elif extension == ".txt":
        return extract_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )