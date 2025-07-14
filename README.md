# File Manager MCP Server

A comprehensive MCP (Model Context Protocol) server for file management operations. This server provides agents and tools with full file system access capabilities through a clean, secure interface.

## Features

- **Complete File Operations**: Read, write, append, delete, copy, move files
- **Directory Management**: Create, delete, list directories with recursive options
- **JSON Support**: Native JSON file reading/writing with automatic serialization
- **Search Capabilities**: Find files by pattern and search within file contents
- **File Information**: Get detailed metadata including size, dates, and type
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Safe Operations**: Built-in error handling and validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mlnima/fileManagerMcpServer
cd fileManagerMcpServer
```

2. Install dependencies:
```bash
uv sync
```

3. The server is ready to use!

## Usage

Add this configuration to your MCP client:

```json
{
  "FileManager": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "mcp[cli]",
      "mcp",
      "run",
      "server.py"
    ]
  }
}
```

### Alternative with full path:
```json
{
  "FileManager": {
    "command": "C:\\Users\\user\\.local\\bin\\uv.EXE",
    "args": [
      "run",
      "--with",
      "mcp[cli]",
      "mcp",
      "run",
      "C:\\path\\to\\file-manager-mcp\\server.py"
    ]
  }
}
```

## Available Tools

### File Operations

- **read_file(file_path)** - Read content from any file with automatic encoding detection
- **write_file(file_path, content, overwrite=True)** - Write text content to any file
- **append_file(file_path, content)** - Append content to existing files
- **delete_file(file_path)** - Delete files safely
- **copy_file(source_path, dest_path)** - Copy files with automatic directory creation
- **move_file(source_path, dest_path)** - Move/rename files

### JSON Operations

- **read_json_file(file_path)** - Read and parse JSON files
- **write_json_file(file_path, data, overwrite=True)** - Write dictionaries as formatted JSON

### Directory Operations

- **list_directory(path)** - List files and folders with detailed information
- **create_folder(folder_path)** - Create directories with parent creation
- **delete_folder(folder_path, recursive=False)** - Delete directories safely

### Search Operations

- **find_files(pattern, path)** - Find files matching patterns (*.txt, *config*, etc.)
- **search_in_files(search_term, file_pattern, path)** - Search text within files

### Information

- **get_file_info(file_path)** - Get comprehensive file metadata

## Project Structure

```
file-manager-mcp/
├── server.py                 # Main MCP server entry point
├── models/
│   └── file_model.py        # Core file operations logic
├── controllers/
│   └── file_controller.py   # MCP tool registration and handling
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Architecture

This project follows the MVC (Model-View-Controller) pattern:

- **Model** (`file_model.py`): Core file system operations with error handling
- **Controller** (`file_controller.py`): MCP tool registration and response formatting
- **Server** (`server.py`): FastMCP server initialization and startup

## Security Features

- Automatic parent directory creation for safe file operations
- Comprehensive error handling and validation
- Multiple encoding support for text file reading
- Safe path resolution to prevent directory traversal

## Dependencies

- `fastmcp` - MCP server framework
- `pathlib` - Modern path handling
- `json` - JSON serialization support
- `shutil` - File operations
- `asyncio` - Async support for Windows

## Examples

### Reading a file:
```python
# Agent can call: read_file("/path/to/document.txt")
# Returns: file content as string
```

### Writing JSON data:
```python
# Agent can call: write_json_file("/path/to/config.json", {"key": "value"})
# Returns: confirmation with bytes written
```

### Finding files:
```python
# Agent can call: find_files("*.py", "/project/src")
# Returns: list of all Python files in the directory
```

### Searching in files:
```python
# Agent can call: search_in_files("TODO", "*.py", "/project")
# Returns: list of Python files containing "TODO"
```

## Error Handling

All operations return structured responses with success/error status. The server handles:
- File not found errors
- Permission denied errors
- Invalid path errors
- Encoding issues
- JSON parsing errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details