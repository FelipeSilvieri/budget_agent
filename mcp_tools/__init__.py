"""Tool registry for the Quotation Generator."""

from fastmcp import FastMCP

from .generate_quote import register as register_generate_quote


mcp = FastMCP(
    name="Quotation Generator",
    instructions="Uma tool que orquestra a geração de orçamentos para clientes.",
)

register_generate_quote(mcp)

__all__ = ["mcp"]
