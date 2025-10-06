# RAG for PDFs — Demo (Free-first)


**Features**
- Upload multiple PDFs
- Vector search with `all-MiniLM-L6-v2` (384-dim)
- Output modes: 5p / 15p summaries (map-reduce), Chapters, Q&A
- Export to PDF (ReportLab)
- Two modes:
- **Free local** (no API keys): T5-small summarization & extractive-ish Q&A
- **OpenAI** (optional): set `OPENAI_API_KEY` for higher quality (gpt-4o-mini)


## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY= # optional
python app.py
```


## Deploy to Hugging Face Spaces (free demo)
1. Create new Space (SDK: **Gradio**)
2. Add these files; set Space secrets: `OPENAI_API_KEY` (optional)
3. Space auto-builds; share the public URL.


## Notes
- For large PDFs, performance depends on CPU. You can raise `target_chars` in `chunk_text()` for fewer chunks.
- For production: persist FAISS index, add reranking, background jobs, and object storage.
"""
