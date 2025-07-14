import json
from typing import List, Dict, Any
from models.fileModel import FileManager  # Updated import

# Note: This file uses the camelCase naming convention as requested, which differs
# from Python's standard PEP 8 style (snake_case).

class FileController:
    """
    Acts as the controller layer for the MCP server, bridging the gap between
    the MCP tool definitions and the underlying file system logic in FileManager.

    It registers each file operation as a distinct tool, formats the results
    from FileManager into human-readable strings, and handles the success
    and error cases for the MCP agent.
    """
    def __init__(self, mcp: Any):
        """
        Initializes the FileController.

        :param mcp: The main MCP server instance used to register tools.
        """
        self.mcp = mcp
        self.fileManager = FileManager()  # Use the refactored FileManager
        self.tools: List = []
        self._registerTools()

    def _registerTools(self):
        """
        A private method to define and register all file management tools with the MCP server.
        Each tool is a wrapper around a FileManager method, providing clear descriptions
        and user-friendly output.
        """

        @self.mcp.tool()
        def readFile(filePath: str) -> str:
            """
            Reads the entire content of a specified file and returns it as a string.
            This tool automatically handles various common text encodings.

            :param filePath: The absolute or relative path to the file to be read.
            :return: The full content of the file on success, or an error message on failure.
            """
            result = self.fileManager.readFile(filePath)
            return result.get("content", result.get("error", "An unknown error occurred."))

        @self.mcp.tool()
        def writeFile(filePath: str, content: str, overwrite: bool = True) -> str:
            """
            Writes string content to a specified file. Creates parent directories if they don't exist.
            By default, it overwrites existing files.

            :param filePath: The path where the file will be written.
            :param content: The string content to write to the file.
            :param overwrite: Set to False to prevent overwriting an existing file.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.writeFile(filePath, content, overwrite)
            if result["success"]:
                return f"Successfully wrote {result['bytesWritten']} bytes to {result['path']}"
            return result["error"]

        @self.mcp.tool()
        def appendFile(filePath: str, content: str) -> str:
            """
            Appends string content to the end of a file. If the file doesn't exist, it will be created.

            :param filePath: The path to the file to which content will be appended.
            :param content: The string content to append.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.appendFile(filePath, content)
            if result["success"]:
                return f"Successfully appended {result['bytesAppended']} bytes to {result['path']}"
            return result["error"]

        @self.mcp.tool()
        def deleteFile(filePath: str) -> str:
            """
            Deletes a single file from the system. This operation cannot be undone.
            To delete a directory, use the `deleteFolder` tool.

            :param filePath: The path to the file to be deleted.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.deleteFile(filePath)
            if result["success"]:
                return f"Successfully deleted file: {result['deleted']}"
            return result["error"]

        @self.mcp.tool()
        def copyFile(sourcePath: str, destPath: str) -> str:
            """
            Copies a file from a source path to a destination path, preserving metadata.
            Creates parent directories for the destination if they don't exist.

            :param sourcePath: The path of the file to copy.
            :param destPath: The destination path for the new file.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.copyFile(sourcePath, destPath)
            if result["success"]:
                return f"Successfully copied {result['copiedFrom']} to {result['copiedTo']}"
            return result["error"]

        @self.mcp.tool()
        def moveFile(sourcePath: str, destPath: str) -> str:
            """
            Moves or renames a file from a source path to a destination path.
            Creates parent directories for the destination if they don't exist.

            :param sourcePath: The current path of the file.
            :param destPath: The new path for the file.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.moveFile(sourcePath, destPath)
            if result["success"]:
                return f"Successfully moved {result['movedFrom']} to {result['movedTo']}"
            return result["error"]

        @self.mcp.tool()
        def getFileInfo(path: str) -> str:
            """
            Retrieves detailed information about a file or directory as a JSON string.
            Includes size, modification/creation times, type, and full path.

            :param path: The path to the file or directory.
            :return: A JSON string with file details on success, or an error message on failure.
            """
            result = self.fileManager.getFileInfo(path)
            if result["success"]:
                info = {k: v for k, v in result.items() if k != "success"}
                return json.dumps(info, indent=2)
            return result["error"]

        @self.mcp.tool()
        def writeJsonFile(filePath: str, data: Dict, overwrite: bool = True) -> str:
            """
            Writes a Python dictionary to a file as a formatted JSON string.
            Handles JSON serialization and file writing in one step.

            :param filePath: The path where the JSON file will be saved.
            :param data: The dictionary to serialize and write.
            :param overwrite: Set to False to prevent overwriting an existing file.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.writeJsonFile(filePath, data, overwrite)
            if result["success"]:
                return f"Successfully wrote JSON data to {result['path']} ({result['bytesWritten']} bytes)"
            return result["error"]

        @self.mcp.tool()
        def readJsonFile(filePath: str) -> str:
            """
            Reads a JSON file and returns its parsed content as a formatted JSON string.
            Useful for inspecting structured data files.

            :param filePath: The path to the JSON file.
            :return: A JSON string of the file's data on success, or an error message on failure.
            """
            result = self.fileManager.readJsonFile(filePath)
            if result["success"]:
                return json.dumps(result.get("data"), indent=2)
            return result["error"]

        @self.mcp.tool()
        def listDirectory(path: str) -> str:
            """
            Lists the contents of a directory, showing each item's type, name, size, and modification date.

            :param path: The path to the directory to list.
            :return: A formatted string listing directory contents, or an error message.
            """
            result = self.fileManager.listDirectory(path)
            if result["success"]:
                if not result["items"]:
                    return f"Directory is empty: {path}"
                # Format output for better readability
                headers = {"Type": 4, "Size": 10, "Modified": 19, "Name": 0}
                lines = [f"{'Type':<5} {'Size':>10} {'Modified':<20} {'Name'}"]
                lines.append(f"{'-'*4:<5} {'-'*10:>10} {'-'*19:<20} {'-'*4}")
                for item in result["items"]:
                    size_str = f"{item['size']}"
                    lines.append(f"{item['type']:<5} {size_str:>10} {item['modified'].split('T')[0]:<20} {item['name']}")
                return "\n".join(lines)
            return result["error"]

        @self.mcp.tool()
        def createFolder(folderPath: str) -> str:
            """
            Creates a new directory at the specified path. Creates parent directories as needed.

            :param folderPath: The path of the directory to create.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.createFolder(folderPath)
            if result["success"]:
                return f"Successfully created folder: {result['created']}"
            return result["error"]

        @self.mcp.tool()
        def deleteFolder(folderPath: str, recursive: bool = False) -> str:
            """
            Deletes a directory. By default, it only deletes empty directories.
            This operation cannot be undone.

            :param folderPath: The path of the directory to delete.
            :param recursive: Set to True to delete the directory and all of its contents.
            :return: A confirmation message on success, or an error message on failure.
            """
            result = self.fileManager.deleteFolder(folderPath, recursive)
            if result["success"]:
                return f"Successfully deleted folder: {result['deleted']} (recursive: {result['recursive']})"
            return result["error"]

        @self.mcp.tool()
        def findFiles(pattern: str, path: str) -> str:
            """
            Recursively finds files and directories matching a glob pattern (e.g., '*.txt', 'data_??.csv').

            :param pattern: The glob pattern to search for.
            :param path: The root directory to start the search from.
            :return: A formatted list of all matches, or an error message.
            """
            result = self.fileManager.findFiles(pattern, path)
            if result["success"]:
                if not result["matches"]:
                    return f"No files found matching pattern '{pattern}' in path '{path}'"
                return "\n".join([f"{match['path']}" for match in result["matches"]])
            return result["error"]

        @self.mcp.tool()
        def searchInFiles(searchTerm: str, filePattern: str, path: str) -> str:
            """
            Recursively searches for a case-insensitive text string within files matching a pattern.

            :param searchTerm: The text string to search for.
            :param filePattern: A glob pattern to identify which files to search in (e.g., '*.py', '*.log').
            :param path: The root directory to start the search from.
            :return: A list of files containing the search term, or an error message.
            """
            result = self.fileManager.searchInFiles(searchTerm, filePattern, path)
            if result["success"]:
                if not result["files"]:
                    return f"Search term '{searchTerm}' not found in any files matching '{filePattern}' in path '{path}'"
                return "\n".join([match["file"] for match in result["files"]])
            return result["error"]

        # Update the list of tools with the new camelCase function names
        self.tools = [
            readFile, writeFile, appendFile, deleteFile, copyFile, moveFile,
            getFileInfo, writeJsonFile, readJsonFile, listDirectory,
            createFolder, deleteFolder, findFiles, searchInFiles
        ]

    def getTools(self) -> List:
        """
        Returns the list of registered tool functions.

        :return: A list of all tool functions available in this controller.
        """
        return self.tools