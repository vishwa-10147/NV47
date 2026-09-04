from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def is_safe_path(path: Path) -> bool:
    try:
        path.resolve().relative_to(PROJECT_ROOT.resolve())
        return True
    except ValueError:
        return False


def list_files(relative_path: str = ".") -> dict:
    target = (PROJECT_ROOT / relative_path).resolve()

    if not is_safe_path(target):
        return {
            "success": False,
            "message": "Access denied: path is outside the NV001 project",
        }

    if not target.exists():
        return {
            "success": False,
            "message": "Directory does not exist",
        }

    if not target.is_dir():
        return {
            "success": False,
            "message": "Path is not a directory",
        }

    files = []

    for item in sorted(target.iterdir()):
        files.append(
            {
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
            }
        )

    return {
        "success": True,
        "path": str(target),
        "files": files,
    }


def read_file(relative_path: str) -> dict:
    target = (PROJECT_ROOT / relative_path).resolve()

    if not is_safe_path(target):
        return {
            "success": False,
            "message": "Access denied: path is outside the NV001 project",
        }

    if not target.exists():
        return {
            "success": False,
            "message": "File does not exist",
        }

    if not target.is_file():
        return {
            "success": False,
            "message": "Path is not a file",
        }

    try:
        content = target.read_text(encoding="utf-8")

        return {
            "success": True,
            "path": str(target),
            "content": content,
        }

    except UnicodeDecodeError:
        return {
            "success": False,
            "message": "This is not a supported UTF-8 text file",
        }