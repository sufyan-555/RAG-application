from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


class Data():
    def __init__(
            self,
            embedding_model,
            data_dir,
            database_dir,
            chunk_size,
            chunk_overlap
        ):


        self.embedding_model=embedding_model
        self.data_dir=data_dir
        self.database_dir=database_dir
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        print("Class init")

    def load(self):
        self.data_loader=PyPDFDirectoryLoader(
            path=self.data_dir
        )
        self.data=self.data_loader.load()
        print("Data Loaded")

    def chunk(self):
        self.text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        self.data_chunks=self.text_splitter.split_documents(self.data)
        print("Data Chunked")

    def database(self):
        self.vector_db=Chroma.from_documents(
            documents=self.data_chunks,
            embedding=self.embedding_model,
        persist_directory=self.database_dir
        )
        print("Database Created")

    def return_db(self):
        return self.vector_db.as_retriever()

    
## ERROR module pwd not found, was coming so i commented out the 
## import pwd in the source file