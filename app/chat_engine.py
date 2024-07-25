from langchain_together.embeddings import TogetherEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_together import Together
from fastapi import HTTPException
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)

load_dotenv()
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

def get_answer(question, chat_history):
    """
    Generates an answer for the given question using a conversational retrieval model.

    Args:
        question (str): The question to generate an answer for.
        chat_history (list): The chat history as a list of previous messages.

    Returns:
        str: The generated answer.

    Raises:
        HTTPException: If an error occurs while generating the answer.
    """
    try:
        logger.info("Generating answer for question: %s", question)
        embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval")
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        llm = Together(
            temperature=0, 
            model="meta-llama/Llama-3-70b-chat-hf",
            together_api_key=TOGETHER_API_KEY,
            max_tokens=1000
        )
        
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )
        
        result = qa_chain({"question": question, "chat_history": chat_history})
        logger.info("Answer generated successfully for question: %s", question)
        return result['answer']
    except Exception as e:
        logger.error("Error generating answer: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))