An interactive chatbot that let's you upload PDFs and extract instant answers and summaries using LLMs.

## 🚀 Quick Start
Start the project in 3 steps
```bash
#1. Clone the repository
git clone https://github.com/hajuanas92-code/pdf-qa-assistant.git

#2. Navigete to the project folder
cd pdf-qa-assistant

#3. Install the libraries
pip install -r requirements.txt

#4. Run the app
python pdf_rag.py

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

1. Create a file named `.env` in the root directory of your project.
2. Add your Grok API key inside the file:
