# PDFQueryBot

This is a robust PDF chatbot application that allows users to upload PDF files and chat with their contents using the Together API with the Llama 3 70B model. It is designed to provide an interactive and user-friendly way to extract information from PDFs.

## Features

- **PDF Upload and Processing**: Users can upload PDF files which are processed to create embeddings for efficient querying.
- **Conversational Interface**: Users can interact with the contents of the PDF in a conversational manner, making it easy to extract relevant information.
- **Rate Limiting**: To ensure fair usage and prevent abuse, the application includes rate limiting.
- **Error Handling and Logging**: Comprehensive error handling and logging mechanisms are in place to ensure smooth operation and easy debugging.
- **Unit Tests**: Includes unit tests to ensure the reliability and correctness of the application.

![image](https://github.com/user-attachments/assets/d6317c8d-61e6-4c81-95de-5f604b733309)


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/NabidAkhtar/PDFQueryBot.git
    cd PDFQueryBot
    ```

2. Install the requirements using:
    ```sh
    pip install -r requirements.txt
    ```

3. Configuration
The application configuration is managed through the Config class in app/config.py, which defines several key settings:

- TOGETHER_API_KEY: API key for accessing the Together service, necessary for generating responses.
- UPLOAD_FOLDER: Directory path for storing uploaded files, ensuring that files are organized and accessible.
- MAX_UPLOAD_SIZE: Maximum allowed size for uploaded files (10 MB), preventing excessively large uploads that could impact performance.
- ALLOWED_EXTENSIONS: Set of allowed file extensions for uploads (currently only 'pdf'), ensuring that only valid file types are processed.
- RATE_LIMIT: Rate limit for API requests (5 requests per minute), helping to manage server load and prevent abuse.

## Usage

1. **Running the Application**:
    ```sh
    uvicorn main:app --host 127.0.0.1 --port 8000
    ```

2. **Uploading a PDF**:
    - Endpoint: `/upload-pdf/`
    - Method: `POST`
    - Parameters: `file` (UploadFile)

3. **Chatting with PDF Contents**:
    - Endpoint: `/chat/`
    - Method: `POST`
    - Parameters: `question` (string)

## Code Overview

### `main.py`

This is the main entry point of the application. It sets up the FastAPI app, including middleware, rate limiting, and routes for uploading PDFs and chatting.

- **Logging**: Configures logging to capture detailed logs of the application's operations.
- **Rate Limiting**: Uses `slowapi` to implement rate limiting to prevent abuse.
- **CORS**: Configures CORS to allow cross-origin requests.
- **PDF Upload Route** (`/upload-pdf/`): Handles PDF uploads, checks file validity and size, saves the file, and processes it.
- **Chat Route** (`/chat/`): Handles chat queries, generates responses using the Together API, and constructs chat history.

## Example Request

- **Upload PDF**:
    ```sh
    curl -X POST "http://127.0.0.1:8000/upload-pdf/" -F "file=@your-file.pdf"
    ```

- **Chat with PDF**:
    ```sh
    curl -X POST "http://127.0.0.1:8000/chat/" -H "Content-Type: application/json" -d '{"question": "What is the main topic of the PDF?"}'
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

---

