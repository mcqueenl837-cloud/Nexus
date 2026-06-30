NEXUS
Navigate knowledge the way textbooks actually build it.

The Idea:
While i was studying  from my Classical Mechanics textbook, i came across a problem . Textbooks have references for Topics,Equations and Figures, they are mentioned in nearby texts. When we try to find that cross-refrences within the books it takes a lot of time to gather them resulting in the wastage of time that could be used for studying further topics.

What Nexus Does:

Nexus is a Retrieval-Augmented Generation (RAG) application designed to answer questions from a **text-based PDF textbook** with high accuracy while minimizing hallucinations.
When a textbook is uploaded, Nexus first extracts its text using PyMuPDF. It then uses the PDF's Table of Contents (TOC) to identify where the actual chapters begin, ignoring front matter such as the cover page, copyright page, preface, and index.

The extracted content is stored in a JSON file where each key represents a page number and its corresponding value contains the complete text of that page.
Next, Nexus analyzes the textbook using **Regular Expressions (Regex)** to identify the structure of the book. It recognizes chapter headings, equations, and figure captions through their numbering patterns, such as  Equation 7.8, Eq. 8.1, or Figure 9.1. For every topic it discovers, Nexus also searches the surrounding text to build relationships between topics, equations, and figures, creating a structured knowledge map of the textbook.

The extracted information is stored in the following format:
Topic->Topic Content->Related Topics,Equations and Figures
This structured data is converted into vector embeddings using a pre-trained embedding model and stored in ChromaDB. When a user asks a question, Nexus performs a cosine similarity search to retrieve only the most relevant sections of the textbook. These retrieved passages, along with the user's question, are then sent to the language model with a carefully designed prompt.

Unlike general-purpose AI assistants, Nexus does not send the entire textbook to the language model.
For example, a 600-page textbook can easily require more than 500,000 tokens, which exceeds the context window of most language models and significantly increases token usage. Sending such a large amount of information is both inefficient and more likely to produce hallucinations.

What Makes Nexus Different?

Dependency Chain Detection:
Nexus doesn't retrieve isolated paragraphs. It builds a dependency chain by identifying related topics, equations, and figures, allowing the AI to understand the connections between concepts instead of treating each section independently.

Model-Agnostic Design:
Nexus is independent of any specific Large Language Model. The retrieval pipeline is separated from the language model, allowing Groq, OpenAI, Claude, Gemini, or any compatible LLM to be integrated without changing the core architecture.

Optimized Token Usage:
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





