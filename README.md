An interactive chatbot that let's you upload PDFs and extract instant answers and summaries using LLMs.

## ✨ Features
* **PDF Text Extraction:** Extracts text from uploaded pdf document using `pypdf`.
* **Local EMBEDDINGS:** `Sentence-Transformers` to generate highle accurate sentence embeddings
* **Fast vector search:** `FAISS` (Facebook AI Similarity Search) for finding accurate content
* **Advance AI response:** Connects `Grok API` to `transformers` to create answer from the retrieved context

## Tech Stack
* **Document Parsing:** `pypdf`
* **Embeddings Model:** `sentence-transformers`
* **Vector Database:** `FAISS`
* **LLM Integration:** `transformers` & Grok API
* **Language:** Python 3.8+

## ⚙️ Configuration
This project requires a Grok API key to generate chat responses. 


