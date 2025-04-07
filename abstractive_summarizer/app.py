import streamlit as st
from summarizer import summarize
from newspaper import Article

st.set_page_config(page_title="Abstractive Summarizer", layout="centered")
st.title("📝 Abstractive Text Summarizer")
st.caption("Summarize large documents or URLs using transformer-based models.")

# Input options
input_type = st.radio("Choose input method:", ["Paste Text", "Upload .txt File", "Enter URL"])
text = ""

if input_type == "Paste Text":
    text = st.text_area("Paste your content here:", height=300)

elif input_type == "Upload .txt File":
    uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

elif input_type == "Enter URL":
    url = st.text_input("Paste article/blog URL here")
    if url:
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            st.success("✅ Article text extracted.")
        except Exception as e:
            st.error(f"❌ Failed to extract article: {e}")

# Preview
if text:
    st.subheader("📄 Input Preview")
    st.text(text[:1000] + ("..." if len(text) > 1000 else ""))

# Summary length controls
max_len = st.slider("Max summary length per chunk (tokens)", 300, 1024, 500)
min_len = st.slider("Min summary length per chunk (tokens)", 100, 800, 200)

# Trigger summarization
if st.button("Generate Summary"):
    if len(text.strip().split()) < 50:
        st.warning("⚠️ Please enter at least 50 words for a meaningful summary.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize(text, max_len, min_len)
            st.subheader("🔍 Summary")
            st.markdown(summary)
