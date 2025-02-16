import os
import json
import glob
from typing import List, Dict
from datetime import datetime
from pathlib import Path
import subprocess
from app.config import settings

class FileService:
    def __init__(self):
        self.data_dir = settings.DATA_DIR

    def read_file(self, path: str) -> str:
        """Read file content safely from the data directory."""
        full_path = self._ensure_safe_path(path)
        with open(full_path, 'r') as f:
            return f.read()

    def write_file(self, path: str, content: str) -> None:
        """Write content to a file safely in the data directory."""
        full_path = self._ensure_safe_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

    def _ensure_safe_path(self, path: str) -> str:
        """Ensure the path is within the data directory."""
        full_path = os.path.abspath(os.path.join(self.data_dir, path.lstrip('/')))
        if not full_path.startswith(self.data_dir):
            raise ValueError("Access denied: Path outside data directory")
        return full_path

    def get_recent_logs(self, log_dir: str, count: int = 10) -> List[str]:
        """Get the first lines of the most recent log files."""
        log_path = self._ensure_safe_path(log_dir)
        log_files = glob.glob(os.path.join(log_path, "*.log"))
        recent_files = sorted(log_files, key=os.path.getmtime, reverse=True)[:count]
        
        first_lines = []
        for file in recent_files:
            with open(file, 'r') as f:
                first_lines.append(f.readline().strip())
        return first_lines

    def extract_markdown_titles(self, directory: str) -> Dict[str, str]:
        """Extract H1 titles from markdown files."""
        dir_path = self._ensure_safe_path(directory)
        md_files = glob.glob(os.path.join(dir_path, "**/*.md"), recursive=True)
        
        titles = {}
        for file in md_files:
            relative_path = os.path.relpath(file, dir_path)
            with open(file, 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith('# '):
                        titles[relative_path] = line.lstrip('# ').strip()
                        break
        return titles

    async def format_markdown(self, file_path: str) -> None:
        """Format markdown file using prettier."""
        full_path = self._ensure_safe_path(file_path)
        try:
            subprocess.run(['npx', 'prettier@3.4.2', '--write', full_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to format markdown: {str(e)}")

file_service = FileService()