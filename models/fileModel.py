import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class FileManager:
    def __init__(self):
        pass

    def _safeRead(self, filePath: Path) -> str:
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                return filePath.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"Cannot decode file: {filePath}")

    def readFile(self, filePath: str) -> Dict[str, Any]:
        targetPath = Path(filePath).resolve()
        if not targetPath.exists():
            return {"success": False, "error": f"File does not exist: {filePath}"}

        try:
            content = self._safeRead(targetPath)
            return {"success": True, "content": content, "size": len(content.encode('utf-8'))}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def writeFile(self, filePath: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        targetPath = Path(filePath).resolve()

        if targetPath.exists() and not overwrite:
            return {"success": False, "error": f"File exists and overwrite=False: {filePath}"}

        try:
            targetPath.parent.mkdir(parents=True, exist_ok=True)
            targetPath.write_text(content, encoding='utf-8')
            bytesWritten = len(content.encode('utf-8'))
            return {"success": True, "bytesWritten": bytesWritten, "path": str(targetPath)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def appendFile(self, filePath: str, content: str) -> Dict[str, Any]:
        targetPath = Path(filePath).resolve()

        try:
            targetPath.parent.mkdir(parents=True, exist_ok=True)
            with open(targetPath, 'a', encoding='utf-8') as f:
                f.write(content)
            bytesAppended = len(content.encode('utf-8'))
            return {"success": True, "bytesAppended": bytesAppended, "path": str(targetPath)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def deleteFile(self, filePath: str) -> Dict[str, Any]:
        targetPath = Path(filePath).resolve()

        if not targetPath.exists():
            return {"success": False, "error": f"File does not exist: {filePath}"}

        if targetPath.is_dir():
            return {"success": False, "error": f"Use deleteFolder for directories: {filePath}"}

        try:
            targetPath.unlink()
            return {"success": True, "deleted": str(targetPath)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def copyFile(self, sourcePath: str, destPath: str) -> Dict[str, Any]:
        source = Path(sourcePath).resolve()
        dest = Path(destPath).resolve()

        if not source.exists():
            return {"success": False, "error": f"Source file does not exist: {sourcePath}"}

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            return {"success": True, "copiedFrom": str(source), "copiedTo": str(dest)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def moveFile(self, sourcePath: str, destPath: str) -> Dict[str, Any]:
        source = Path(sourcePath).resolve()
        dest = Path(destPath).resolve()

        if not source.exists():
            return {"success": False, "error": f"Source file does not exist: {sourcePath}"}

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(dest))
            return {"success": True, "movedFrom": str(source), "movedTo": str(dest)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def getFileInfo(self, filePath: str) -> Dict[str, Any]:
        targetPath = Path(filePath).resolve()

        if not targetPath.exists():
            return {"success": False, "error": f"File does not exist: {filePath}"}

        try:
            stat = targetPath.stat()
            return {
                "success": True,
                "path": str(targetPath),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "isDir": targetPath.is_dir(),
                "isFile": targetPath.is_file(),
                "extension": targetPath.suffix
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def writeJsonFile(self, filePath: str, data: dict, overwrite: bool = True) -> Dict[str, Any]:
        try:
            jsonContent = json.dumps(data, indent=2, ensure_ascii=False)
            return self.writeFile(filePath, jsonContent, overwrite)
        except Exception as e:
            return {"success": False, "error": f"Failed to serialize JSON: {str(e)}"}

    def readJsonFile(self, filePath: str) -> Dict[str, Any]:
        result = self.readFile(filePath)
        if not result["success"]:
            return result

        try:
            data = json.loads(result["content"])
            return {"success": True, "data": data}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}

    def listDirectory(self, path: str) -> Dict[str, Any]:
        targetPath = Path(path).resolve()

        if not targetPath.exists():
            return {"success": False, "error": f"Path does not exist: {path}"}

        try:
            items = []
            for item in sorted(targetPath.iterdir()):
                itemInfo = {
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0,
                    "path": str(item)
                }
                items.append(itemInfo)

            return {"success": True, "items": items, "count": len(items)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def createFolder(self, folderPath: str) -> Dict[str, Any]:
        targetPath = Path(folderPath).resolve()

        try:
            targetPath.mkdir(parents=True, exist_ok=True)
            return {"success": True, "created": str(targetPath)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def deleteFolder(self, folderPath: str, recursive: bool = False) -> Dict[str, Any]:
        targetPath = Path(folderPath).resolve()

        if not targetPath.exists():
            return {"success": False, "error": f"Folder does not exist: {folderPath}"}

        if not targetPath.is_dir():
            return {"success": False, "error": f"Not a directory: {folderPath}"}

        try:
            if recursive:
                shutil.rmtree(targetPath)
                return {"success": True, "deleted": str(targetPath), "recursive": True}
            else:
                targetPath.rmdir()
                return {"success": True, "deleted": str(targetPath), "recursive": False}
        except OSError as e:
            if not recursive and targetPath.exists():
                return {"success": False, "error": f"Directory not empty: {folderPath}"}
            return {"success": False, "error": str(e)}

    def findFiles(self, pattern: str, path: str) -> Dict[str, Any]:
        targetPath = Path(path).resolve()

        if not targetPath.exists():
            return {"success": False, "error": f"Path does not exist: {path}"}

        try:
            matches = list(targetPath.rglob(pattern))
            results = []
            for match in matches:
                results.append({
                    "path": str(match),
                    "name": match.name,
                    "type": "dir" if match.is_dir() else "file",
                    "size": match.stat().st_size if match.is_file() else 0
                })

            return {"success": True, "matches": results, "count": len(results)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def searchInFiles(self, searchTerm: str, filePattern: str, path: str) -> Dict[str, Any]:
        targetPath = Path(path).resolve()

        if not targetPath.exists():
            return {"success": False, "error": f"Path does not exist: {path}"}

        try:
            matches = []

            for filePath in targetPath.rglob(filePattern):
                if filePath.is_file():
                    try:
                        content = self._safeRead(filePath)
                        if searchTerm.lower() in content.lower():
                            matches.append({
                                "file": str(filePath),
                                "name": filePath.name
                            })
                    except:
                        continue

            return {"success": True, "files": matches, "count": len(matches)}
        except Exception as e:
            return {"success": False, "error": str(e)}