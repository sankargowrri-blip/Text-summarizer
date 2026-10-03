import streamlit as st
from transformers import pipeline
import re
import time
from collections import Counter

# PDF support
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📝 AI-Based Text Summarizer")

st.write(
    "An intelligent abstractive text summarization system "
    "using a pretrained Transformer model."
)

st.info(
    "Enter text, upload a TXT/PDF file, select your preferred "
    "summary settings, and generate a concise summary."
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_summarizer():

    model = pipeline(
        "summarization",
        model="sshleifer/distilbart-xsum-12-6"
    )

    return model


# ============================================================
# SAMPLE TEXT
# ============================================================

sample_text = """
Artificial Intelligence is one of the most important technologies
in the modern world. It allows computers and machines to perform
tasks that normally require human intelligence. These tasks include
learning, reasoning, problem solving, understanding natural language,
recognizing images and making decisions.

Machine learning is a major part of Artificial Intelligence.
Machine learning algorithms learn patterns from data and use those
patterns to make predictions or decisions. Deep learning is another
important area that uses neural networks with multiple layers.

Artificial Intelligence is widely used in healthcare, education,
banking, transportation, agriculture, manufacturing and entertainment.
In healthcare, AI can help doctors analyze medical images and identify
possible diseases. In education, AI can provide personalized learning
experiences for students.

Although Artificial Intelligence provides many benefits, it also
creates challenges such as privacy, security, bias and job
displacement. Therefore, AI should be developed and used responsibly.
"""


# ============================================================
# SESSION STATE
# ============================================================

if "text" not in st.session_state:
    st.session_state.text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "keywords" not in st.session_state:
    st.session_state.keywords = []


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Summarization Settings")

summary_length = st.sidebar.selectbox(
    "Summary Length",
    [
        "Short",
        "Medium",
        "Detailed"
    ]
)

summary_format = st.sidebar.radio(
    "Summary Format",
    [
        "Paragraph",
        "Bullet Points"
    ]
)

st.sidebar.markdown("---")

st.sidebar.header("🔧 Text Processing")

remove_extra_spaces = st.sidebar.checkbox(
    "Remove extra spaces",
    value=True
)

remove_special_characters = st.sidebar.checkbox(
    "Clean special characters",
    value=False
)

st.sidebar.markdown("---")

st.sidebar.header("ℹ️ About")

st.sidebar.write(
    "This application uses the "
    "DistilBART Transformer model for "
    "abstractive text summarization."
)


# ============================================================
# FILE UPLOAD
# ============================================================

st.subheader("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a TXT or PDF file",
    type=["txt", "pdf"]
)

uploaded_text = ""

if uploaded_file is not None:

    if uploaded_file.type == "text/plain":

        try:

            uploaded_text = uploaded_file.getvalue().decode(
                "utf-8"
            )

            st.success(
                "TXT file uploaded successfully."
            )

        except Exception:

            st.error(
                "Unable to read the TXT file."
            )

    elif uploaded_file.type == "application/pdf":

        if PDF_AVAILABLE:

            try:

                pdf_reader = PyPDF2.PdfReader(
                    uploaded_file
                )

                pages = []

                for page in pdf_reader.pages:

                    page_text = page.extract_text()

                    if page_text:
                        pages.append(page_text)

                uploaded_text = "\n".join(pages)

                st.success(
                    f"PDF uploaded successfully. "
                    f"Pages: {len(pdf_reader.pages)}"
                )

            except Exception as e:

                st.error(
                    f"Unable to read PDF: {e}"
                )

        else:

            st.error(
                "PyPDF2 is not installed. "
                "Run: pip install PyPDF2"
            )


# ============================================================
# TEXT INPUT
# ============================================================

st.subheader("✍️ Enter Text")

user_text = st.text_area(
    "Paste your article, notes or paragraph here:",
    value=uploaded_text if uploaded_text else st.session_state.text,
    height=300,
    placeholder="Enter your text here..."
)

st.session_state.text = user_text


# ============================================================
# BUTTONS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "🧪 Load Example",
        use_container_width=True
    ):

        st.session_state.text = sample_text

        st.rerun()


with col2:

    if st.button(
        "🗑️ Clear",
        use_container_width=True
    ):

        st.session_state.text = ""
        st.session_state.summary = ""
        st.session_state.keywords = []

        st.rerun()


with col3:

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        st.session_state.text = ""
        st.session_state.summary = ""
        st.session_state.keywords = []

        st.rerun()


# ============================================================
# TEXT PREPROCESSING
# ============================================================

def clean_text(text):

    text = text.strip()

    if remove_extra_spaces:

        text = re.sub(
            r"\s+",
            " ",
            text
        )

    if remove_special_characters:

        text = re.sub(
            r"[^A-Za-z0-9.,!?;:'\"()\-\s]",
            "",
            text
        )

    return text


processed_text = clean_text(
    st.session_state.text
)


# ============================================================
# TEXT STATISTICS
# ============================================================

words = processed_text.split()

word_count = len(words)

character_count = len(processed_text)

sentence_count = len(
    re.findall(
        r"[.!?]+",
        processed_text
    )
)

paragraph_count = len(
    [
        p for p in processed_text.split("\n")
        if p.strip()
    ]
)

reading_time = (
    word_count / 200
    if word_count > 0
    else 0
)


# ============================================================
# DISPLAY INPUT STATISTICS
# ============================================================

st.markdown("---")

st.subheader("📊 Text Statistics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Words",
    word_count
)

c2.metric(
    "Characters",
    character_count
)

c3.metric(
    "Sentences",
    sentence_count
)

c4.metric(
    "Paragraphs",
    paragraph_count
)

c5.metric(
    "Reading Time",
    f"{reading_time:.1f} min"
)


# ============================================================
# SUMMARY SETTINGS
# ============================================================

length_settings = {

    "Short": {
        "max": 60,
        "min": 15
    },

    "Medium": {
        "max": 100,
        "min": 25
    },

    "Detailed": {
        "max": 150,
        "min": 40
    }
}


max_length = length_settings[
    summary_length
]["max"]

min_length = length_settings[
    summary_length
]["min"]


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text, number=10):

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower()
    )

    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "which",
        "their",
        "there",
        "about",
        "these",
        "those",
        "using",
        "into",
        "they",
        "will",
        "been",
        "also",
        "more",
        "than",
        "such",
        "where",
        "when",
        "what",
        "would",
        "could",
        "should",
        "while",
        "your",
        "some",
        "other",
        "only",
        "used",
        "uses"
    }

    filtered = [
        word
        for word in words
        if word not in stop_words
    ]

    frequency = Counter(filtered)

    return [
        word
        for word, count in frequency.most_common(number)
    ]


# ============================================================
# GENERATE SUMMARY
# ============================================================

if st.button(
    "✨ Generate AI Summary",
    type="primary",
    use_container_width=True
):

    if not processed_text:

        st.warning(
            "Please enter some text or upload a document."
        )

    elif word_count < 20:

        st.warning(
            "Please enter at least 20 words "
            "for better summarization."
        )

    else:

        try:

            start_time = time.time()

            with st.spinner(
                "🤖 AI is generating your summary..."
            ):

                summarizer = load_summarizer()

                result = summarizer(
                    processed_text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )

                generated_summary = result[
                    0
                ][
                    "summary_text"
                ]

            processing_time = (
                time.time() - start_time
            )

            # ------------------------------------
            # Bullet Point Format
            # ------------------------------------

            if summary_format == "Bullet Points":

                sentences = re.split(
                    r"(?<=[.!?])\s+",
                    generated_summary
                )

                generated_summary = "\n".join(
                    [
                        "• " + sentence.strip()
                        for sentence in sentences
                        if sentence.strip()
                    ]
                )

            st.session_state.summary = (
                generated_summary
            )

            st.session_state.keywords = (
                extract_keywords(processed_text)
            )

            st.success(
                "Summary generated successfully!"
            )

            st.caption(
                f"Processing Time: "
                f"{processing_time:.2f} seconds"
            )

        except Exception as e:

            st.error(
                f"Error while generating summary: {e}"
            )


# ============================================================
# DISPLAY SUMMARY
# ============================================================

if st.session_state.summary:

    st.markdown("---")

    st.subheader("📄 Generated Summary")

    st.text_area(
        "Summary",
        value=st.session_state.summary,
        height=200
    )


    # ========================================================
    # SUMMARY STATISTICS
    # ========================================================

    summary_text = (
        st.session_state.summary
        .replace("• ", "")
    )

    summary_words = len(
        summary_text.split()
    )

    compression = (
        (
            1 -
            summary_words /
            word_count
        ) * 100
        if word_count > 0
        else 0
    )


    st.subheader(
        "📈 Summary Analysis"
    )

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Original Words",
        word_count
    )

    s2.metric(
        "Summary Words",
        summary_words
    )

    s3.metric(
        "Compression",
        f"{compression:.1f}%"
    )


    # ========================================================
    # KEYWORDS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔑 Important Keywords"
    )

    if st.session_state.keywords:

        keyword_text = " • ".join(
            st.session_state.keywords
        )

        st.write(
            keyword_text
        )


    # ========================================================
    # ORIGINAL VS SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔍 Original vs Summary"
    )

    left, right = st.columns(2)

    with left:

        st.write(
            "**Original Text**"
        )

        st.write(
            processed_text
        )

    with right:

        st.write(
            "**AI Summary**"
        )

        st.write(
            st.session_state.summary
        )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.markdown("---")

    st.subheader(
        "💾 Download Summary"
    )

    st.download_button(
        label="⬇️ Download Summary as TXT",
        data=st.session_state.summary,
        file_name="AI_Text_Summary.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.markdown("---")

with st.expander(
    "ℹ️ About This Project"
):

    st.write(
        """
        **Project Title:**
        Abstractive Text Summarizer using Transformer Model

        **Technology Used:**
        Python, Streamlit, Hugging Face Transformers and PyTorch.

        **Dataset:**
        XSum (Extreme Summarization) dataset.

        **Main Function:**
        The system converts long input text into a shorter
        meaningful summary using abstractive text generation.

        **Additional Features:**
        • TXT file upload
        • PDF file upload
        • Text statistics
        • Keyword extraction
        • Summary length control
        • Bullet-point summaries
        • Compression analysis
        • Reading-time estimation
        • Summary download
        • Cloud deployment support
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI-Based Text Summarizer | "
    "Python + Streamlit + Hugging Face Transformers"
)
