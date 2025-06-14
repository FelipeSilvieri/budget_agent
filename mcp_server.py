from mcp_tools import mcp

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
