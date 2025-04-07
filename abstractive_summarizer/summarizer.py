import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from transformers import pipeline

# Load BART summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, max_words=700):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def format_as_bullets(text):
    # Turn summary into bullet list
    sentences = text.replace("\n", " ").split(". ")
    bullet_points = [f"- {s.strip().rstrip('.')}" for s in sentences if len(s.strip()) > 0]
    return "\n".join(bullet_points)

def summarize(text, max_len=500, min_len=200):
    if not text or len(text.strip().split()) < 50:
        return "❗ Input text is too short for summarization."

    try:
        chunks = chunk_text(text)
        all_summaries = []

        for chunk in chunks:
            result = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
            if isinstance(result, list) and "summary_text" in result[0]:
                formatted = format_as_bullets(result[0]['summary_text'])
                all_summaries.append(formatted)

        return "\n\n".join(all_summaries) if all_summaries else "⚠️ No summary generated."
    
    except Exception as e:
        return f"❌ Error during summarization: {str(e)}"
