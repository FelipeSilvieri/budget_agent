from fastmcp import BaseTool
from pydantic import BaseModel
from typing import List, Optional

from services.doc_service import BudgetItem, BudgetRequest, generate_document


class GenerateQuoteInput(BaseModel):
    cliente: Optional[str] = None
    responsavel: Optional[str] = None
    proposta_comercial: Optional[str] = None
    email: Optional[str] = None
    data: Optional[str] = None
    assunto: Optional[str] = None
    itens: List[BudgetItem]


class GenerateQuoteTool(BaseTool):
    name = "generate_quote"
    description = "Cria um documento de orçamento em DOCX"
    input_model = GenerateQuoteInput

    def run(self, data: GenerateQuoteInput) -> str:
        req = BudgetRequest(**data.model_dump())
        return generate_document(req)
