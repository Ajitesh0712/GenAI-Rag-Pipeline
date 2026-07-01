from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services.indexer import index_document
from pydantic import BaseModel
from services.rag import ask_rag

from services.document_manager import list_documents
from services.document_manager import delete_document

from fastapi import UploadFile, File, HTTPException
from pathlib import Path
import shutil
app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    try:

        filename = Path(file.filename).name

        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        save_path = UPLOAD_DIR / filename

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )
        chunk_count = index_document(
            str(save_path)
        )
        return {
            "success": True,
            "filename": filename,
            "chunks":chunk_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(
    request: ChatRequest
):
    try:

        result = ask_rag(
            request.message
        )

        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
    
@app.get("/documents")
async def get_documents():
    return {
        "success": True,
        "documents": list_documents()
    }

@app.delete("/documents/{filename}")
async def delete_document_api(filename: str):

    deleted = delete_document(filename)

    return {
        "success": True,
        "deleted_chunks": deleted
    }