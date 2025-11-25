import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional
from ..utils.repository_analyzer import RepositoryAnalyzer


class GitHubReaderTool:
    """Tool for cloning GitHub repositories to a temporary directory.
    
    This tool focuses solely on repository cloning and cleanup operations.
    All analysis functionality is handled by the agent layer.
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize the GitHub Reader tool.
        
        Args:
            project_root: Root directory of the project. If None, uses current working directory.
        """
        self.name = "github_reader"
        
        # Set up temp directory for cloned repositories
        if project_root is None:
            project_root = os.getcwd()
        self.temp_dir = Path(project_root) / "temp" / "github_clones"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize analyzer for URL parsing
        self._analyzer = RepositoryAnalyzer()
    
    def clone_repo(self, repo_url: str, force: bool = False) -> str:
        """Clone a GitHub repository to the temp directory.
        
        This is the primary tool function exposed to the agent.
        
        Args:
            repo_url: The URL of the GitHub repository
            force: If True, remove existing clone and re-clone
            
        Returns:
            String message with clone status and path
        """
        try:
            owner, repo = self._analyzer._parse_repo_url(repo_url)
            clone_path = self.temp_dir / owner / repo
            
            # Check if already cloned
            if clone_path.exists():
                if force:
                    shutil.rmtree(clone_path)
                else:
                    return f"Repository already cloned at: {clone_path}"
            
            # Create parent directory
            clone_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Clone the repository
            result = subprocess.run(
                ["git", "clone", repo_url, str(clone_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                return f"Error: Git clone failed - {result.stderr}"
            
            return f"Successfully cloned {owner}/{repo} to: {clone_path}"
            
        except ValueError as e:
            return f"Error: {str(e)}"
        except subprocess.TimeoutExpired:
            return "Error: Clone operation timed out (exceeded 5 minutes)"
        except Exception as e:
            return f"Error cloning repository: {str(e)}"
    
    def cleanup_repo(self, repo_url: str) -> str:
        """Remove a cloned repository from the temp directory.
        
        Args:
            repo_url: The URL of the GitHub repository
            
        Returns:
            String message with cleanup status
        """
        try:
            owner, repo = self._analyzer._parse_repo_url(repo_url)
            clone_path = self.temp_dir / owner / repo
            
            if not clone_path.exists():
                return f"Repository not found at {clone_path}"
            
            shutil.rmtree(clone_path)
            return f"Successfully removed {owner}/{repo}"
            
        except Exception as e:
            return f"Error cleaning up repository: {str(e)}"
    
    def cleanup_all(self) -> str:
        """Remove all cloned repositories from the temp directory.
        
        Returns:
            String message with cleanup status
        """
        try:
            if not self.temp_dir.exists():
                return "No repositories to clean up"
            
            # Count repos before cleanup
            repo_count = sum(1 for _ in self.temp_dir.rglob("*/.git"))
            
            shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
            return f"Successfully removed {repo_count} repositories"
            
        except Exception as e:
            return f"Error cleaning up all repositories: {str(e)}"
