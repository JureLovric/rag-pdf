SYSTEM = (
"You are a precise technical editor. Be concise, structured, and faithful to the provided context."
)


SUMMARIZE_SECTION = (
"""
You will receive a batch of context chunks from a longer PDF. Write a concise summary
covering only salient facts. Avoid repetition. Output Markdown.
Desired tone: informative, neutral.
"""
)


REDUCE_PROMPT = (
"""
You will receive a list of section summaries. Merge them into a coherent document with
clear headings and bullets. Preserve factuality; do not hallucinate beyond content.
Output Markdown.
"""
)


QNA_PROMPT = (
"""
Answer the user's question strictly using the provided context. If the answer is not
contained, say "I couldn't find this in the document." Keep to 3-6 sentences.
"""
)


CHAPTERS_PROMPT = (
"""
Using the provided context, draft a chapterized outline with H2 headings and short
paragraphs under each heading. End with a brief "+ Next Steps" section.
Output Markdown.
"""
)
