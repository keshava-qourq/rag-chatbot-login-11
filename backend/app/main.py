"""Application entrypoint.

Generated from the approved architecture: one router per component that owns
endpoints, one route per endpoint the API spec declares. Every generated route
is a stub that returns a typed placeholder, so the service starts, serves its
OpenAPI document and passes its tests before a single handler is implemented.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401 -- imported so the tables register before create_all
from app.database import Base, engine

app = FastAPI(
    title="# RAG Chatbot Login",
    description="# RAG Chatbot with Login, Chat History and Gemini\n\nBuild a RAG chatbot. Users sign up and log in, upload documents, and ask questions about\nthem. Answers come only from the chosen document. Every chat is saved, so users can come\nback to it later. Use the Google Gemini API (free tier) for embeddings and answers.\n\n## Tech stack\n- Frontend: React.\n- Backend: Python FastAPI with SQLAlchemy.\n- Database: PostgreSQL through DATABASE_URL. When DATABASE_URL is not set, the starter\n  project falls back to SQLite, and the app must work on both. So store embeddings as a\n  JSON list of numbers, not a Postgres-only vector type.\n- Create the tables at startup (Base.metadata.create_all). No migration tool.\n\n## Backend libraries (declare all of these in requirements.txt)\n- google-genai: the Gemini SDK\n- pypdf: read PDF files\n- python-docx: read DOCX files\n- python-multipart: file uploads in FastAPI\n- numpy: cosine similarity search\n- bcrypt: hash passwords\n- PyJWT: login tokens\n\n## Settings (environment variables, never hardcoded)\n- DATABASE_URL: optional. SQLite is used when it is not set.\n- JWT_SECRET: optional. If it is not set, generate a random one at startup and log a\n  warning that users will be logged out on every restart.\n- GEMINI_API_KEY: optional. If it is not set, each user pastes their own key after\n  logging in. The backend keeps it in memory for that user only. It never stores it in\n  the database, logs it, or sends it back.\n- GEMINI_CHAT_MODEL, default \"gemini-2.5-flash\"\n- GEMINI_EMBED_MODEL, default \"gemini-embedding-001\"\n\n## Database tables\n- users: id, email (unique), password_hash, created_at\n- documents: id, user_id, filename, chunk_count, created_at\n- chunks: id, document_id, chunk_index, page (nullable), text, embedding (JSON)\n- chats: id, user_id, document_id, title, created_at\n- messages: id, chat_id, role (\"user\" or \"assistant\"), content, sources (JSON), created_at\nDeleting a document deletes its chunks and chats. Deleting a chat deletes its messages.\nThe u",
    version="0.1.0",
)

# The SPA runs on a different origin than the API, so the browser refuses its calls
# unless that origin is allowed here. In development that is the Vite dev server; when
# deployed, the platform injects the frontend's real URL as ALLOWED_ORIGINS (comma
# separated). Point ALLOWED_ORIGINS at the real thing and nothing else has to change.
_dev_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
_allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins or _dev_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The scaffold ships no migrations, so the tables are created from the models on
# startup. Replace this with Alembic before anything holds data worth keeping.
Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe, and the only route here that is not a stub."""
    return {"status": "ok"}
