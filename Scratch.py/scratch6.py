#final phase streamlit frontend
import base64
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import chromadb
import pymupdf as fitz
import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer


APP_DIR = Path(__file__).resolve().parent
PDF_DIR = APP_DIR / "uploaded_books"
PDF_PATH = PDF_DIR / "current_book.pdf"
PHASE2_JSON = APP_DIR / "phase2_topics.json"
CHROMA_PATH = APP_DIR / "chroma_storage"
COLLECTION_NAME = "book_content"

os.chdir(APP_DIR)

st.set_page_config(
    page_title="Nexus",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background: #0B1120;
            color: #F8FAFC;
        }

        [data-testid="stHeader"] {
            background: rgba(11, 17, 32, 0.90);
        }

        .title {
            font-size: 44px;
            font-weight: 800;
            color: #F8FAFC;
            margin-bottom: 0px;
        }

        .subtitle {
            font-size: 17px;
            color: #CBD5E1;
            margin-bottom: 22px;
        }

        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 12px;
        }

        div.stButton > button {
            background: #111827;
            color: #F8FAFC;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 10px;
        }

        div.stButton > button:hover {
            border-color: #14B8A6;
            color: #38BDF8;
        }

        [data-testid="stFileUploader"] {
            background: #111827;
            border-radius: 10px;
            padding: 10px;
        }

        [data-testid="stChatMessage"] {
            background: #1A2333;
            border: 1px solid rgba(56, 189, 248, 0.18);
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def load_groq_client():
    return Groq(api_key=os.environ.get("GROQ_API_KEY"))


def load_backend_function(file_name, function_name):
    file_path = APP_DIR / file_name
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def save_uploaded_pdf(uploaded_file):
    PDF_DIR.mkdir(exist_ok=True)
    PDF_PATH.write_bytes(uploaded_file.getbuffer())
    st.session_state["page_number"] = 1


def display_pdf():
    if not PDF_PATH.exists():
        st.info("Upload a PDF to preview it here.")
        return

    page_number = st.session_state.get("page_number", 1)

    doc = fitz.open(str(PDF_PATH))
    total_pages = len(doc)

    page_number = max(1, min(page_number, total_pages))
    st.session_state["page_number"] = page_number

    page = doc[page_number - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    image_bytes = pix.tobytes("png")
    doc.close()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    st.markdown(
        f"""
        <div style="width: 100%; overflow-y: auto;">
            <img
                src="data:image/png;base64,{image_base64}"
                style="width: 100%; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.25);"
            />
        </div>
        """,
        unsafe_allow_html=True,
    )


def reset_current_book():
    for file_path in [
        PDF_PATH,
        APP_DIR / "extracted_text1.json",
        APP_DIR / "phase2_topics.json",
    ]:
        if file_path.exists():
            file_path.unlink()

    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    st.session_state["book_ready"] = False
    st.session_state["chat_history"] = []
    st.session_state["uploaded_file_name"] = None
    st.session_state["page_number"] = 1


def run_phase1():
    process_pdf = load_backend_function("scratch2.py", "process_pdf")
    result = process_pdf(str(PDF_PATH))

    if result is None:
        raise RuntimeError("The uploaded PDF may not be text-based.")

    return result


def run_phase2():

    try:

        subprocess.run(
            [sys.executable,str(APP_DIR/"scratch3.py")],
            cwd=str(APP_DIR),
            capture_output=True,
            text=True,
            check=True,
        )

    except subprocess.CalledProcessError as e:

        st.error(
            "This PDF cannot be processed.\n\n"
            "No recognizable chapter headings were found.\n"
            "Please upload another textbook."
        )

        raise RuntimeError("Phase 2 extraction failed.") from e

def prepare_documents(phase2_data):
    ids = []
    documents = []
    metadatas = []

    for topic_key, topic_data in phase2_data.items():
        placement = topic_data["placement"]
        page = topic_data["page"]
        text = topic_data["text"]
        related_content = topic_data.get("related_content", {})

        document_text = f"""
Title: {topic_key}
Placement: {placement}
Page: {page}

Content:
{text}

Related content:
{related_content}
"""

        ids.append(topic_key.replace(" ", "_"))
        documents.append(document_text)
        metadatas.append(
            {
                "topic_key": topic_key,
                "placement": placement,
                "page": page,
            }
        )

    return ids, documents, metadatas


def run_phase3():

    try:

        with PHASE2_JSON.open("r",encoding="utf-8") as file:
            phase2_data=json.load(file)

        if not isinstance(phase2_data,dict) or len(phase2_data)==0:
            st.warning(
                "This PDF could not be processed.\n\n"
                "No topics were extracted from the document.\n"
                "Please upload another textbook."
            )
            return

        ids,documents,metadatas=prepare_documents(phase2_data)

        if len(ids)==0 or len(documents)==0 or len(metadatas)==0:
            st.warning(
                "This PDF could not be processed.\n\n"
                "No valid content was extracted from the document.\n"
                "Please upload another textbook."
            )
            return

        embeddings=load_embedding_model().encode(documents)

        if embeddings is None or len(embeddings)==0:
            st.warning(
                "This PDF could not be processed.\n\n"
                "Embeddings could not be generated.\n"
                "Please upload another textbook."
            )
            return

        chroma_client=chromadb.PersistentClient(path=str(CHROMA_PATH))

        try:
            chroma_client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

        collection=chroma_client.get_or_create_collection(name=COLLECTION_NAME)

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings.tolist(),
        )

    except Exception as e:

        print("Phase 3 Error:",e)

        st.error(
            "This PDF is not supported.\n\n"
            "The document could not be processed because it does not contain enough structured information "
            "to build the knowledge base.\n\n"
            "Please upload another text-based textbook."
        )

        return
def is_text_based_pdf(pdf_path):
    doc = fitz.open(str(pdf_path))

    for page in doc:
        text = page.get_text().strip()

        if len(text) > 50:
            doc.close()
            return True

    doc.close()
    return False

def process_book_pipeline():
    if not is_text_based_pdf(PDF_PATH):
        st.session_state["book_ready"] = False
        st.error(
            "This PDF does not appear to be text-based. It may be image-based or scanned. "
            "Please upload a text-based PDF."
        )
        return

    run_phase1()
    run_phase2()
    run_phase3()
    st.session_state["book_ready"] = True
    run_phase1()
    run_phase2()
    run_phase3()
    st.session_state["book_ready"] = True


def build_prompt(question):
    embedding_model = load_embedding_model()

    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = chroma_client.get_collection(COLLECTION_NAME)

    query_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    best_distance = results["distances"][0][0]

    if best_distance > 1.2:
        return "OUT_OF_BOOK"

    documents = results["documents"][0]
    context = "\n\n".join(documents)

    prompt = f"""Hello Groq, you are a set of teachers, Whose subject depends on the content given to you.
You have to give response like you are teaching a college student. Types of questions you could expect from the user:
1) Relation betweeen certain topics, equations or figure or it could be in the form of relation of certain topic with ceratin equations or figures.
2) Explanation of Topics/Titles, Equations or figures could also be asked.
3) Closest candidates of content related to certain topics/titles, equations or figures. You have to give explain their relation.

Most Important instruction:
- You have to explain by content provided to you. It is usually going to be a set of Three lists.
The three lists are going to be closest content related to what have asked .
Context={context}

Question asked by user={question}

You have to give answer in the format of:
-Question asked by user
-your findings based upon Context given to you.

You have to give answer in range of 100-200 words only. Give more information by expanding the word range
if you think this is not sufficient information for question asked. 
You can give more information when someone asks a long query
or someone asks relation of upto three entities.

"I am unable to find any relevant content as per your question asked. It seems like you have 
asked for something that doesn't exist in the book"

if you find the retrieved data irrevalent

answer:
"""

    return prompt


def ask_backend(prompt):
    if prompt == "OUT_OF_BOOK":
        return (
            "I am unable to find any relevant content as per your question asked. "
            "It seems like you have asked for something that doesn't exist in the book."
        )

    groq_client = load_groq_client()

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


def render_header():
    st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Navigate knowledge the way textbooks actually build it.</div>',
        unsafe_allow_html=True,
    )


def render_pdf_panel():
    st.markdown('<div class="section-title">Textbook Workspace</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload textbook PDF", type=["pdf"])

    if uploaded_file is not None:
        previous_file = st.session_state.get("uploaded_file_name")

        if previous_file != uploaded_file.name:
            reset_current_book()
            st.session_state["uploaded_file_name"] = uploaded_file.name
            save_uploaded_pdf(uploaded_file)

            with st.spinner("Processing book..."):
                process_book_pipeline()

    page_controls = st.columns(3)

    with page_controls[0]:
        if st.button(
            "Previous Page",
            use_container_width=True,
            key="previous_page_button",
        ):
            current_page = st.session_state.get("page_number", 1)
            st.session_state["page_number"] = max(1, current_page - 1)

    with page_controls[1]:
        st.write(f"Page {st.session_state.get('page_number', 1)}")

    with page_controls[2]:
        if st.button(
            "Next Page",
            use_container_width=True,
            key="next_page_button",
        ):
            current_page = st.session_state.get("page_number", 1)
            st.session_state["page_number"] = current_page + 1

    display_pdf()

    if st.button(
        "Delete Current Book",
        use_container_width=True,
        key="delete_current_book_button",
    ):
        reset_current_book()
        st.rerun()


def render_chat_panel():
    st.markdown('<div class="section-title">Chat</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if not st.session_state.get("book_ready"):
        st.info("Upload and process a textbook before asking questions.")

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask about anything")

    if question:
        st.session_state["chat_history"].append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.write(question)

        if not st.session_state.get("book_ready"):
            answer = "Please upload and process a textbook first."
        else:
            with st.spinner("Searching textbook and generating answer..."):
                prompt = build_prompt(question)
                answer = ask_backend(prompt)

        st.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)


def main():
    apply_theme()
    render_header()

    left_column, right_column = st.columns([1.08, 0.92], gap="large")

    with left_column:
        render_pdf_panel()

    with right_column:
        render_chat_panel()


if __name__ == "__main__":
    main()