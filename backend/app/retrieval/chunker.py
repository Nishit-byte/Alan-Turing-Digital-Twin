from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def clean_text(text: str) -> str:
    """Basic cleanup — collapse whitespace, remove page-break artifacts."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'-\n(\w)', r'\1', text)  # fix hyphenated line breaks
    return text.strip()

def chunk_document(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Split cleaned text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)

def process_document(file_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    """
    Full pipeline: load a document (PDF or .txt) -> clean -> chunk.
    Returns list of dicts with chunk text + metadata.
    """
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        raw_text = extract_text_from_pdf(str(path))
    elif path.suffix.lower() == ".txt":
        raw_text = path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    cleaned = clean_text(raw_text)
    chunks = chunk_document(cleaned, chunk_size, chunk_overlap)

    return [
        {
            "text": chunk,
            "source": path.name,
            "chunk_id": f"{path.stem}_{i}"
        }
        for i, chunk in enumerate(chunks)
    ]