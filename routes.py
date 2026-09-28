from fastapi import APIRouter, HTTPException
from ai_core.gemini_generator import GeminiConfigurationError, GeminiDocumentGenerator, GeminiGenerationError
from backend.schemas import DocumentRequest, DocumentResponse

router = APIRouter()

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    try:
        generator = GeminiDocumentGenerator()
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            language=request.language,
            additional_instructions=request.additional_instructions,
        )
        return DocumentResponse(document_type=request.document_type, content=content, model=generator.model)
    except GeminiConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except GeminiGenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
