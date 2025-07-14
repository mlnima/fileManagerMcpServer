from mcp.server.fastmcp import FastMCP
import asyncio
import sys
from controllers.file_controller import FileController

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

mcp = FastMCP("FileManager")

fileController = FileController(mcp)

print(f"File Manager MCP Server initialized with {len(fileController.getTools())} tools")

if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("Server interrupted")
    except Exception as e:
        print(f"Server error: {e}")