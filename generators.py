from typing import List
)
text = resp.choices[0].message.content
return [text]
# local map over chunks using flan-t5-small as text2text
pipe = _get_local_sum()
outs = []
for c in chunks:
c_short = c[:4000] # safeguard
s = pipe(c_short + "\n\nSummarize the main points succinctly.", max_length=256, do_sample=False)[0]["generated_text"]
outs.append(s)
return outs




def reduce_summaries(parts: List[str]) -> str:
parts = parts or []
if USE_OPENAI and parts:
prompt = REDUCE_PROMPT + "\n\n" + "\n\n".join(f"- {p}" for p in parts)
resp = oai.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
temperature=0.2
)
return resp.choices[0].message.content
# local: simply join with headings
if not parts:
return "# Summary\n\n(No content found in uploaded PDFs.)"
joined = "\n\n".join(f"### Section\n{p}" for p in parts)
return f"## Summary\n\n{joined}"




def answer_question(question: str, contexts: List[str]) -> str:
contexts = contexts or []
if USE_OPENAI and contexts:
prompt = QNA_PROMPT + "\n\nCONTEXT:\n" + "\n\n".join(contexts[:8]) + f"\n\nQUESTION: {question}"
resp = oai.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
temperature=0.1
)
return resp.choices[0].message.content
# local heuristic answer: return top contexts stitched
if not contexts:
return "I couldn't find this in the document."
text = "\n\n".join(contexts[:4])
return f"(Extractive answer from top chunks)\n\n{text}"




def chapterize(contexts: List[str]) -> str:
contexts = contexts or []
if USE_OPENAI and contexts:
prompt = CHAPTERS_PROMPT + "\n\n" + "\n\n".join(contexts[:12])
resp = oai.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
temperature=0.3
)
return resp.choices[0].message.content
# local fallback: headings from first sentences
import re
if not contexts:
return "## Next Steps\nUpload PDFs and rebuild the index."
heads = []
for i, c in enumerate(contexts[:10], 1):
sent = re.split(r"(?<=[.!?])\s+", c.strip())[0]
heads.append(f"## Section {i}\n{sent}\n")
return "\n".join(heads) + "\n\n## Next Steps\nReview the full PDF for details."
