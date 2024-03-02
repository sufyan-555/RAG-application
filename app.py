from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from doc_to_db import Data
from model_functions import *
import streamlit as st
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"]="your_api_key"

data_dir="Documents/"
database_dir="Database/"


embedding_model=HuggingFaceInferenceAPIEmbeddings(
    model_name="sentence-transformers/all-MiniLM-l6-v2",
    api_key="your_api_key"
)

model=HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    
    )


def handle_userinput(model,user_question):
    if not st.session_state.retriever:
        prompt_teplate=get_normal_prompt()
        prompt=prompt_teplate.format(
            question=user_question
        )
        result=process_model_output(model=model,prompt=prompt)
        st.session_state.history=update_history(
            history=st.session_state.history,
            question=user_question,
            answer=result
        )
    else:
        prompt_teplate=get_rag_prompt()
        docs=st.session_state.retriever.get_relevant_documents(user_question)
        content=""
        for doc in docs:
            content+=doc.page_content
        prompt=prompt_teplate.format(
            context=content,
            question=user_question,
            history=st.session_state.history_rag
            )
        result=process_model_output(model,prompt=prompt)
        st.session_state.history_rag=update_history(
            history=st.session_state.history_rag,
            question=user_question,
            answer=result
        )


def main():
    st.set_page_config(
        page_title="RAG Application"
    )

    if "retriever" not in st.session_state:
        st.session_state.retriever=None
    if "history" not in st.session_state:
        st.session_state.history=""
    if "history_rag" not in st.session_state:
        st.session_state.history_rag=""

    
    st.header("Talk to your Pdf")
    st.write("*To delete database enter: DELETE*")
    user_question = st.chat_input("Ask a questions:")
    if user_question:
        if user_question=="DELETE":
            if "retriever" not in st.session_state:
                st.write("Nothing to Delete")
            else:
                st.session_state.retriever.delete_collections()
                st.session_state.retriever.persist()
                st.write("Database Deleted")
        handle_userinput(model,user_question)

        if st.session_state.history_rag=="":
            st.write(st.session_state.history)
        st.write(st.session_state.history_rag)

    with st.sidebar:
        st.subheader("Your documents")

        if not os.path.exists('Documents'):
            os.makedirs('Documents')

        pdf_docs = st.file_uploader("Upload your PDFs here")
        if pdf_docs is not None:
            with open(os.path.join('Documents', pdf_docs.name), "wb") as f:
                f.write(pdf_docs.getbuffer())
                
        if st.button("Process"):
            with st.spinner("Processing"):
                data=Data(
                    embedding_model=embedding_model,
                    data_dir=data_dir,
                    database_dir=database_dir,
                    chunk_overlap=300,
                    chunk_size=2000
                )
                data.load()
                data.chunk()
                st.success("Data Loaded and Chunked")
                data.database()
                st.session_state.retriever=data.return_db()
            st.success("File Processed Successfully!!!")


if __name__ == '__main__':
    main()
