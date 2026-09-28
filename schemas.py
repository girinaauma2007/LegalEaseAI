from pydantic import BaseModel, Field, field_validator
from typing import List

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=5000)
    terms: List[str] = Field(default_factory=list, max_length=50)
    effective_date: str = Field(..., min_length=2, max_length=100)
    language: str = Field(default="English", min_length=2, max_length=50)
    additional_instructions: str = Field(default="", max_length=5000)

    @field_validator("document_type", "parties", "effective_date", "language")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty.")
        return value

    @field_validator("terms")
    @classmethod
    def clean_terms(cls, values: List[str]) -> List[str]:
        return [v.strip() for v in values if v and v.strip()]

class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
