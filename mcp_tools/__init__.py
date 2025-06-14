from fastmcp import FastMCP

from .generate_quote import GenerateQuoteTool


mcp = FastMCP("Quotation Generator")
mcp.add_tool(GenerateQuoteTool())

__all__ = ["mcp", "GenerateQuoteTool"]
