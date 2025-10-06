import gradio as gr
text = load_pdf_text(paths)
chunks_glob = chunk_text(text, target_chars=1500, overlap=200)
idx = RAGIndex()
idx.add(chunks_glob)
if not chunks_glob:
return "Uploaded PDFs contained no extractable text."
return f"Loaded {len(paths)} file(s), created {len(chunks_glob)} chunks."




def do_generate(output_type, question, pages):
if not idx:
return "Please upload PDFs and click \"Build index\" first.", None
if not chunks_glob:
return "No text chunks available. Rebuild the index.", None


target_pages = int(pages) if pages in (5, 15, 10) else int(pages)
target_words = target_pages * WORDS_PER_PAGE


if output_type in ("5-page Summary", "15-page Summary"):
# map-reduce summarize with granularity tied to desired pages
desired_sections = target_pages
parts = []
step = max(1, len(chunks_glob)//max(1, desired_sections))
for i in range(0, len(chunks_glob), step):
batch = chunks_glob[i:i+step]
parts.extend(summarize_batch(batch))
md = reduce_summaries(parts)
md = _trim_to_words(md, int(target_words * 1.15)) # allow slight overflow before pagination
title = f"Summary_{target_pages}p.pdf"
elif output_type == "Chapters":
hits = [c for _,_,c in idx.search("overall themes and structure", k=min(12, len(chunks_glob)))]
md = chapterize(hits)
md = _trim_to_words(md, int(target_words * 1.15))
title = "Chapters.pdf"
else: # Q&A
if not (question or "").strip():
return "Please type a question for Q&A mode.", None
hits = [c for _,_,c in idx.search(question, k=min(12, len(chunks_glob)))]
md = "# Answer\n\n" + answer_question(question, hits) + "\n\n# Sources\n" + "\n\n".join(f"- {shorten(h, 160)}" for h in hits)
title = "QA.pdf"


tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
render_pdf(md, tmp.name)
return md, tmp.name


with gr.Blocks(title="RAG for PDFs (Demo)") as demo:
gr.Markdown(INTRO)
with gr.Row():
with gr.Column():
files = gr.File(label="Upload PDF(s)", file_types=[".pdf"], file_count="multiple")
build = gr.Button("Build index", variant="primary")
status = gr.Markdown("Upload your files to begin.")
with gr.Column():
output_type = gr.Radio(["5-page Summary", "15-page Summary", "Chapters", "Q&A"], value="5-page Summary", label="Output Type")
question = gr.Textbox(label="Question (for Q&A)")
pages = gr.Slider(5, 15, step=10, value=5, label="Summary length (pages)")
go = gr.Button("Generate Output", variant="primary")
with gr.Row():
md_out = gr.Markdown(label="Preview")
pdf_out = gr.File(label="Download PDF")


build.click(build_index, inputs=[files], outputs=[status])
go.click(do_generate, inputs=[output_type, question, pages], outputs=[md_out, pdf_out])


if __name__ == "__main__":
demo.launch()
