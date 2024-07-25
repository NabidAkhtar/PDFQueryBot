import pypdf
from langchain_together.embeddings import TogetherEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import logging

logger = logging.getLogger(__name__)

def process_pdf(file_path):
    try:
        # Extract text from PDF
        with open(file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        # Create embeddings and store in FAISS index
        embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval")

        vectorstore = FAISS.from_texts(chunks, embeddings)
        
        # Save the FAISS index
        vectorstore.save_local("faiss_index")
        logger.info(f"PDF processed and indexed successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error processing PDF {file_path}: {str(e)}")
        raise
