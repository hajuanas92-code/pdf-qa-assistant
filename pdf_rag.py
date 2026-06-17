import streamlit as st
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import faiss
from transformers import pipeline
import numpy as np

st.title("PDF RAG chatbot")
st.header("Upload your pdf and ask any question.")

if "messages" not in st.session_state:
  st.session_state.messages = []
for msg in st.session_state.messages:
  with st.chat_message(msg['role']):
    st.write(msg['content'])
#loading models
@st.cache_resource
def load_models():
  model = SentenceTransformer("all-MiniLM-L6-v2")
  bot =  pipeline('text-generation',model="Qwen/Qwen2.5-0.5B-Instruct")
  return model,bot
model, bot = load_models()

uploaded_file = st.file_uploader('upload_file')

#extracting text from pdf
@st.cache_resource
def built_vector_store(file_text):
  #chunking texts
  chunks = []
  chunk_size = 100
  overlap = 20
  texts = file_text.split()
  i = 0
  while i < len(texts):
     words_slice = texts[i : i + chunk_size]
     words = " ".join(words_slice)
     chunks.append(words)
     i += chunk_size - overlap

  #embedding the chunks
  embeddings = model.encode(chunks)
  dim = embeddings.shape[1]
  index = faiss.IndexFlatL2(dim)
  index.add(np.array(embeddings, dtype='float32'))

  return index,chunks

#saving pdf memory
if 'pdf_processed' not in st.session_state:
  st.session_state['pdf_processed'] = False

index = st.session_state.get('vector_index',None)
chunks = st.session_state.get('pdf_chunks',None)

if uploaded_file and not st.session_state['pdf_processed']:
  with st.spinner("Processing the document..."):
    reader = PdfReader(uploaded_file)
    full_text = ""
    for text in reader.pages:
      full_text += text.extract_text() + "\n"
    index,chunks = built_vector_store(full_text)

    st.session_state['pdf_chunks'] = chunks
    st.session_state['vector_index'] = index

    #setting to True after pdf processed
    st.session_state['pdf_processed'] = True
if st.session_state['pdf_processed']:
  st.success('pdf uploaded')

  #user embedding and query
if user := st.text_input('ASk your question.'):

  st.session_state.messages.append({'role':'user','content':user})
  with st.chat_message("user"):
    st.write(user)

  with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
      user_embed = model.encode([user])
      dis,indx = index.search(np.array(user_embed,dtype='float32'),k=3)
      all_matches = []
      for rank,idx in enumerate(indx[0]):
        if idx != -1:
          all_matches.append(chunks[idx])
      context = "\n".join(all_matches)

      with st.expander("Retrieved Contexts."):
        st.write(context)

      prompt = f"""
You should answer according to the given provided context ONLY don't try to make by your own.
just see the context and create according to it.
If you cannot find a similar context say - 'I don't know'. UNDERSTOOD.
context : {context}
question : {user}
answer"""
      chat_history = [{'role':'system','content':prompt}]
      for msg in st.session_state.messages:
        chat_history.append({'role':msg['role'],'content':msg['content']})

      response = bot(
        chat_history,max_new_tokens = 150,return_full_text=False
      )

      answer_text = response[0]['generated_text']
      st.write(answer_text)

      st.session_state.messages.append({'role':'assistant','content':answer_text})