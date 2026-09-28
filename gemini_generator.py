from google import genai
from google.genai import types
from backend.config import settings

class GeminiConfigurationError(RuntimeError):
    pass

class GeminiGenerationError(RuntimeError):
    pass

class GeminiDocumentGenerator:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        if not self.api_key:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured. Add it to the .env file."
            )
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as exc:
            raise GeminiConfigurationError(f"Could not initialize Gemini client: {exc}") from exc

    @staticmethod
    def _build_prompt(document_type, parties, terms, effective_date, language, additional_instructions):
        term_block = "\n".join(f"- {term}" for term in terms) or "- No additional terms supplied."
        return f"""You are a careful legal-document drafting assistant.

Create a professional DRAFT legal document in {language}.
Document type: {document_type}
Parties: {parties}
Effective date: {effective_date}

Requested terms:
{term_block}

Additional instructions:
{additional_instructions or "None"}

Requirements:
1. Use only facts supplied by the user. Never invent names, addresses, amounts, dates, laws, citations, or obligations.
2. Structure the document with a clear title and numbered sections.
3. Include placeholders such as [INSERT AMOUNT] where information is missing.
4. Include signature blocks when appropriate.
5. Use plain but formal legal language.
6. Do not claim that the document is legally valid in a particular jurisdiction.
7. Do not provide legal advice or cite laws unless the user supplied the relevant law.
8. Return only the document draft, without Markdown fences or commentary.
"""

    def generate_document(self, document_type, parties, terms, effective_date, language="English", additional_instructions=""):
        prompt = self._build_prompt(document_type, parties, terms, effective_date, language, additional_instructions)
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=7000,
                    candidate_count=1,
                ),
            )
            text = (response.text or "").strip()
            if not text:
                raise GeminiGenerationError("Gemini returned an empty response.")
            return text
        except GeminiGenerationError:
            raise
        except Exception as exc:
            raise GeminiGenerationError(f"Gemini generation failed: {exc}") from exc
