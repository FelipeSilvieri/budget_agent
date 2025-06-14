try:
    from mcp_tools import mcp
except ModuleNotFoundError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "Missing dependencies. Run `pip install -r requirements.txt`."
    ) from exc

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
