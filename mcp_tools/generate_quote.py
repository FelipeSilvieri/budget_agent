from services.doc_service import BudgetRequest

from fastmcp import FastMCP
from services.doc_service import generate_document

def register(mcp: FastMCP) -> None:
    """Register the ``generate_quote`` tool with the given server."""
    
    @mcp.tool(name="generate_quote", description="Cria um documento de orçamento em DOCX")
    def generate_quote(request: BudgetRequest) -> str:
        """Create a DOCX quote and return the relative file path."""
        return generate_document(request)


__all__ = ["register"]
