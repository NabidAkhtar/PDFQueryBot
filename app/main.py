import os
import sys
import logging
from fastapi.responses import ORJSONResponse


# To allow imports from sibling modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.models import Query, ChatHistory
from app.config import Config
from app.pdf_processor import process_pdf
from app.chat_engine import get_answer

# Create logs directory if it doesn't exist
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Set up logging with relative path
log_file_path = os.path.join(log_dir, 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.post("/upload-pdf/")
@limiter.limit("5/minute")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    """
    Uploads a PDF file, processes it, and creates embeddings.

    Args:
        request (Request): The incoming request object.
        file (UploadFile): The PDF file to be uploaded.

    Returns:
        ORJSONResponse: The response containing the status of the upload and processing.

    Raises:
        ORJSONResponse: If the file format is invalid or the file size exceeds the maximum limit.
        ORJSONResponse: If there is an error processing the PDF.
    """
    try:
        if not allowed_file(file.filename):
            return ORJSONResponse(content={"detail": "Invalid file format. Please upload a PDF."}, status_code=400)
        
        file_size = await file.read()
        await file.seek(0)  # Reset file pointer to the beginning
        
        if len(file_size) > Config.MAX_UPLOAD_SIZE:
            return ORJSONResponse(content={"detail": "File too large. Maximum size is 10 MB."}, status_code=400)
        
        # Create uploads directory if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        file_location = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file_size)
        
        # Process the PDF and create embeddings
        process_pdf(file_location)
        
        logger.info("PDF uploaded and processed successfully: %s", file.filename)
        return ORJSONResponse(content={"message": "PDF uploaded and processed successfully"}, status_code=200)
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return ORJSONResponse(content={"detail": str(e)}, status_code=500)
    
@app.post("/chat/")
async def chat(query: Query):
    try:
        logging.info("Received query: %s", query.question)
        
        # Ensure get_answer is only called once
        response = get_answer(query.question, [])
        logging.info("Generated response: %s", response)
        
        # Construct chat history properly
        chat_history = [
            {"role": "user", "content": query.question},
            {"role": "assistant", "content": response}
        ]
        
        return ORJSONResponse(content={
            "answer": response,
            "chat_history": chat_history
        }, status_code=200)
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)