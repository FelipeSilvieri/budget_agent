"""Generate quotation document tool."""

from typing import List, Optional

from fastmcp import FastMCP

from services.doc_service import BudgetItem, BudgetRequest, generate_document


def register(mcp: FastMCP) -> None:
    """Register the ``generate_quote`` tool with the given server."""

    @mcp.tool(
        name="generate_quote", description="Cria um documento de orçamento em DOCX"
    )
    def generate_quote(
        cliente: Optional[str] = None,
        responsavel: Optional[str] = None,
        proposta_comercial: Optional[str] = None,
        email: Optional[str] = None,
        data: Optional[str] = None,
        assunto: Optional[str] = None,
        itens: List[BudgetItem] = [],
    ) -> str:
        """Create a DOCX quote and return the relative file path."""

        req = BudgetRequest(
            cliente=cliente,
            responsavel=responsavel,
            proposta_comercial=proposta_comercial,
            email=email,
            data=data,
            assunto=assunto,
            itens=itens,
        )
        return generate_document(req)


__all__ = ["register"]
