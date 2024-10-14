import io
import fitz
import urllib.request
from gentopia.tools.basetool import *

class PDFExtractorParams(BaseModel):
    document_url: str = Field(..., description="URL of the PDF document to be processed")

class PDFExtractor(BaseTool):
    name = "pdf_extractor"
    description = "Retrieves a PDF document from a given URL and extracts its textual content"

    args_schema: Optional[Type[BaseModel]] = PDFExtractorParams

    def fetch_document(self, url: str) -> bytes:
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except Exception as e:
            raise ValueError(f"Failed to retrieve document: {str(e)}")

    def extract_text(self, pdf_content: bytes) -> str:
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            return text_content
        except Exception as e:
            raise ValueError(f"Text extraction failed: {str(e)}")

    def _run(self, document_url: str) -> str:
        try:
            pdf_content = self.fetch_document(document_url)
            full_text = self.extract_text(pdf_content)
            return full_text[:1000] + "..." if len(full_text) > 1000 else full_text
        except Exception as e:
            return f"Operation failed: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous operation is not supported")