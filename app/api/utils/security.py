import os
from pathlib import Path
from typing import List
from app.config import settings

class SecurityUtils:
    @staticmethod
    def validate_path(path: str) -> bool:
        """
        Validate if a path is within the allowed data directory and not attempting
        directory traversal.
        """
        try:
            full_path = os.path.abspath(os.path.join(settings.DATA_DIR, path.lstrip('/')))
            return full_path.startswith(settings.DATA_DIR)
        except Exception:
            return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to prevent directory traversal and other security issues.
        """
        return os.path.basename(filename)

    @staticmethod
    def get_safe_paths(paths: List[str]) -> List[str]:
        """
        Convert a list of paths to their safe absolute paths within the data directory.
        Raises ValueError if any path is outside the data directory.
        """
        safe_paths = []
        for path in paths:
            full_path = os.path.abspath(os.path.join(settings.DATA_DIR, path.lstrip('/')))
            if not full_path.startswith(settings.DATA_DIR):
                raise ValueError(f"Invalid path: {path}")
            safe_paths.append(full_path)
        return safe_paths

security_utils = SecurityUtils()