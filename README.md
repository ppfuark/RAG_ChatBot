
RAG Chatbot Platform
====================

This is a fullstack application that implements a RAG-based chatbot using custom PDF/document files as knowledge base. It includes:

- Backend: Built with FastAPI, includes CRUD for managing files used as data source.
- Frontend: A React interface that allows interaction with the chatbot.
- RAG Engine: Uses embeddings + Chroma vector store to answer questions with context from uploaded documents.

Project Structure
-----------------
```
├── backend
    ├── api/                   # FastAPI routes (v1)
    ├── chroma/                # Chroma vector store database
    ├── core/                  # Core logic (embedding, RAG, db)
    ├── data/                  # Uploaded files (PDFs, etc.)
    ├── models/                # Pydantic or DB models
    ├── schemas/               # Request/response schemas
    ├── main.py                # Entrypoint for FastAPI server
    └── requirements.txt       # Python dependencies

└── frontend
    ├── public/                # Static files
    ├── src/
    │   ├── components/        # React components
    │   ├── pages/             # Chat page
    │   └── main.jsx           # React app entry
    └── vite.config.js         # Vite configuration
```

Features
--------
Backend (FastAPI)
- CRUD for documents: Upload and manage files used for context.
- RAG API: Chat endpoint that:
  - Loads context from Chroma DB.
  - Embeds question and finds relevant chunks.
  - Returns LLM-generated answer based on context.

Frontend (React + Vite)
- Clean UI for chatting.
- Sidebar with file upload/management (CRUD).
- Real-time integration with RAG backend.

Setup Instructions
------------------

Backend
1. Navigate to backend:
   cd backend
  
2. Create virtual environment and activate:
   py -m venv .venv
   .venv\Scripts\activate
   
3. Install dependencies:
   pip install -r requirements.txt

4. Run the server:
   uvicorn main:app --reload

Backend will be available at http://localhost:8000

Frontend
1. Navigate to frontend:
   cd frontend

2. Install dependencies:
   npm install

3. Run the dev server:
   npm run dev

Frontend will be available at http://localhost:3000

How RAG Works Here
------------------
1. File Upload: You upload a PDF file through the frontend.
2. Chunking & Embedding: The backend parses and splits the document, generates vector embeddings.
3. Storage: Embeddings are stored using Chroma DB.
4. Querying: When a question is asked, its embedding is compared to stored vectors.
5. Response: Most relevant chunks are passed to an LLM to generate a contextual answer.

