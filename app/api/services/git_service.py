import git
import os
from app.config import settings

class GitService:
    def __init__(self):
        self.data_dir = settings.DATA_DIR

    def clone_repository(self, repo_url: str, target_dir: str) -> str:
        """Clone a git repository to a specific directory."""
        full_path = os.path.join(self.data_dir, target_dir.lstrip('/'))
        os.makedirs(full_path, exist_ok=True)
        
        try:
            repo = git.Repo.clone_from(repo_url, full_path)
            return full_path
        except git.GitCommandError as e:
            raise RuntimeError(f"Failed to clone repository: {str(e)}")

    def create_commit(self, repo_path: str, files: list, message: str) -> str:
        """Create a commit with specified files and message."""
        full_path = os.path.join(self.data_dir, repo_path.lstrip('/'))
        
        try:
            repo = git.Repo(full_path)
            repo.index.add(files)
            commit = repo.index.commit(message)
            return commit.hexsha
        except git.GitCommandError as e:
            raise RuntimeError(f"Failed to create commit: {str(e)}")

git_service = GitService()