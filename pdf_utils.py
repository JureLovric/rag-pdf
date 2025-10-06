from typing import List
from pypdf import PdfReader
import re


def load_pdf_text(paths: List[str]) -> str:
texts = []
for p in paths or []:
try:
reader = PdfReader(p)
except Exception:
continue
parts = []
for page in reader.pages:
try:
parts.append(page.extract_text() or "")
except Exception:
parts.append("")
texts.append("\n\n".join(parts))
return "\n\n".join(texts)


_whitespace = re.compile(r"\s+")


def clean_text(t: str) -> str:
return _whitespace.sub(" ", t or "").strip()


def chunk_text(text: str, target_chars: int = 1500, overlap: int = 200) -> List[str]:
text = clean_text(text)
if not text:
return []
chunks = []
start = 0
n = len(text)
while start < n:
end = min(start + target_chars, n)
# try to end on sentence boundary
slice_ = text[start:end]
last_period = slice_.rfind('.')
if last_period != -1 and end < n and last_period > target_chars * 0.6:
end = start + last_period + 1
chunks.append(text[start:end])
start = max(end - overlap, 0) + overlap
return [c for c in chunks if c.strip()]
