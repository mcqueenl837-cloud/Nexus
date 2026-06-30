## NEXUS
**Navigate knowledge the way textbooks actually build it.**

## The Idea
While i was studying  from my Classical Mechanics textbook, i came across a problem . Textbooks have references for Topics,Equations and Figures, they are mentioned in nearby texts. When we try to find that cross-refrences within the books it takes a lot of time to gather them resulting in the wastage of time that could be used for studying further topics.

## How It Works

**Phase 1 — Extraction**
Uses PyMuPDF's `get_toc()` to find the table of contents and 
locate the page where actual content begins, skipping front 
matter like the preface and copyright pages. Every page's text 
is saved to a JSON dictionary, with page numbers as keys.

**Phase 2 — Mapping**
Regex identifies topics, equations, and figures by their naming 
patterns (e.g. "3.2", "Equation 7.8", "Fig 9.1") and scans 
nearby text for cross-references between them. The result is a 
structured map: topic → content → related topics, equations, 
and figures.

**Phase 3 — Embeddings**
Each piece of content is converted into a vector embedding 
using a pre-trained sentence-transformer model and stored in 
ChromaDB.

**Phase 4 — Retrieval and Response**
When you ask a question, Nexus finds the closest matches via 
cosine similarity, builds a prompt containing only that relevant 
content, and sends it to Groq for an explanation.

**Why this matters:** sending an entire 600-page book to an LLM 
can mean 500,000+ tokens of context — most of it irrelevant to 
your question, and a real driver of hallucination. By retrieving 
only what's relevant, Nexus keeps the context small and grounded,
which is the core idea behind RAG (Retrieval Augmented Generation).

## What Makes Nexus Different?

**Dependency Chain Detection:**
Nexus doesn't retrieve isolated paragraphs. It builds a dependency chain by identifying related topics, equations, and figures, allowing the AI to understand the connections between concepts instead of treating each section independently.

**Model-Agnostic Design:**
Nexus is independent of any specific Large Language Model. The retrieval pipeline is separated from the language model, allowing Groq, OpenAI, Claude, Gemini, or any compatible LLM to be integrated without changing the core architecture.

**Optimized Token Usage:**
Instead of sending an entire textbook to the LLM, Nexus retrieves only the most relevant content. This significantly reduces token usage, lowers inference cost, and improves response efficiency.

## Tech Stack

| Library / Tool              | Purpose                                                                                   | Why I Chose It                                                                  |
| --------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Python                      | Core programming language used to build the entire application.                           | Offers a rich ecosystem for AI, data processing, and rapid development.         |
| Streamlit                   | Builds the web interface for uploading textbooks and interacting with Nexus.              | Makes it easy to develop and deploy AI applications with minimal frontend code. |
| PyMuPDF                     | Extracts text and the Table of Contents (TOC) from PDF textbooks.                         | Fast, reliable, and provides direct access to PDF structure and page content.   |
| Regular Expressions (Regex) | Detects topics, equations, and figure captions based on textbook formatting patterns.     | Efficiently extracts structured information without requiring machine learning. |
| JSON                        | Stores extracted pages, topic mappings, and intermediate processing results.              | Lightweight, portable, and ideal for structured data exchange.                  |
| Sentence Transformers       | Generates semantic vector embeddings from textbook content.                               | Produces high-quality embeddings for semantic search and retrieval.             |
| ChromaDB                    | Stores vector embeddings and retrieves relevant textbook content using cosine similarity. | Lightweight vector database designed for Retrieval-Augmented Generation (RAG).  |
| Groq API                    | Generates responses using the retrieved textbook context.                                 | Provides fast LLM inference while keeping the system model-agnostic.            |
| NumPy                       | Handles embedding arrays and numerical data operations.                                   | Efficient numerical computing for machine learning workflows.                   |
| Base64                      | Encodes PDF files for browser rendering.                                                  | Enables embedded PDF viewing directly inside the Streamlit application.         |
| Pathlib                     | Manages project files and directory paths.                                                | Provides clean, platform-independent file handling.                             |
| Subprocess                  | Executes different processing phases from the main application.                           | Keeps the extraction pipeline modular and organized.                            |
| Importlib                   | Dynamically imports project modules at runtime.                                           | Allows a flexible and modular project structure.                                |
| OS                          | Performs file and directory management operations.                                        | Simplifies filesystem interactions across the project.                          |


## How To Run

1. Clone the repository
git clone https://github.com/mcqueen1837-cloud/Nexus.git
cd Nexus

2. Install dependencies
pip install -r requirements.txt

3. Add your API keys
Create a file named `.env` in the project folder and add:
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
You can get a free Groq API key at:
https://console.groq.com/keys
You can get a free Hugging Face token at:
https://huggingface.co/settings/tokens

4. Run the app
streamlit run scratch6.py

5. Open your browser
Streamlit will automatically open at http://localhost:8501

## Live Demo
https://dreamproject.streamlit.app/

## Limitations

**Only text-based pdf works for this project.**

**No conversation memory of chatbot**

**Single book support per session**

## Future additions

**OCR(optical character recognition) for mapping of image scanned based Pdf.**

**Conversation memory within a chatbot, would possess ability to remember conversation within one chat**

## About me

**I am a 5th semster BSc Physics student at PDEU,Gandhinagar,Gujarat.
I built this project to solve my personal problem during my studying session.**   









  

