from fastmcp import FastMCP

from .generate_quote import GenerateQuoteTool


mcp = FastMCP(
    name="Quotation Generator",
    description="Uma tool que orquestra a geração de orçamentos para clientes.",
)
mcp.add_tool(GenerateQuoteTool())

__all__ = ["mcp", "GenerateQuoteTool"]
