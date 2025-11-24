import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional

class GitHubReaderTool:
    def __init__(self, project_root: Optional[str] = None):
        """Initialize the GitHub Reader tool.
        
        Args:
            project_root: Root directory of the project. If None, uses current working directory.
        """
        self.name = "github_reader"
        self.api_base = "https://api.github.com"
        
        # Set up temp directory for cloned repositories
        if project_root is None:
            project_root = os.getcwd()
        self.temp_dir = Path(project_root) / "temp" / "github_clones"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def _parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """Parse GitHub URL to extract owner and repo name.
        
        Args:
            repo_url: GitHub repository URL (HTTPS or SSH)
            
        Returns:
            Tuple of (owner, repo_name)
            
        Raises:
            ValueError: If URL is invalid
        """
        # Remove .git suffix if present
        repo_url = repo_url.rstrip("/").replace(".git", "")
        
        # Handle HTTPS URLs: https://github.com/owner/repo
        if "github.com/" in repo_url:
            parts = repo_url.split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        # Handle SSH URLs: git@github.com:owner/repo
        if "git@github.com:" in repo_url:
            parts = repo_url.split("git@github.com:")[-1].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    
    def clone_repo(self, repo_url: str, force: bool = False) -> Dict[str, any]:
        """Clone a GitHub repository to the temp directory.
        
        Args:
            repo_url: The URL of the GitHub repository
            force: If True, remove existing clone and re-clone
            
        Returns:
            Dictionary with status, message, and clone_path
        """
        try:
            owner, repo = self._parse_repo_url(repo_url)
            clone_path = self.temp_dir / owner / repo
            
            # Check if already cloned
            if clone_path.exists():
                if force:
                    shutil.rmtree(clone_path)
                else:
                    return {
                        "status": "exists",
                        "message": f"Repository already cloned at {clone_path}",
                        "clone_path": str(clone_path)
                    }
            
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
                return {
                    "status": "error",
                    "message": f"Git clone failed: {result.stderr}",
                    "clone_path": None
                }
            
            return {
                "status": "success",
                "message": f"Successfully cloned {owner}/{repo}",
                "clone_path": str(clone_path)
            }
            
        except ValueError as e:
            return {"status": "error", "message": str(e), "clone_path": None}
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Clone operation timed out", "clone_path": None}
        except Exception as e:
            return {"status": "error", "message": f"Error cloning repo: {e}", "clone_path": None}
    
    def analyze_cloned_repo(self, repo_url: str) -> Dict[str, any]:
        """Analyze a cloned repository and return comprehensive information.
        
        Args:
            repo_url: The URL of the GitHub repository
            
        Returns:
            Dictionary with repository analysis
        """
        try:
            owner, repo = self._parse_repo_url(repo_url)
            clone_path = self.temp_dir / owner / repo
            
            if not clone_path.exists():
                return {
                    "status": "error",
                    "message": f"Repository not cloned. Call clone_repo() first."
                }
            
            analysis = {
                "status": "success",
                "owner": owner,
                "repo": repo,
                "clone_path": str(clone_path),
                "structure": self._get_directory_structure(clone_path),
                "key_files": self._read_key_files(clone_path),
                "stats": self._get_repo_stats(clone_path)
            }
            
            return analysis
            
        except Exception as e:
            return {"status": "error", "message": f"Error analyzing repo: {e}"}
    
    def _get_directory_structure(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> List[str]:
        """Get directory structure up to max_depth.
        
        Args:
            path: Path to analyze
            max_depth: Maximum depth to traverse
            current_depth: Current depth (used in recursion)
            
        Returns:
            List of file/directory paths relative to root
        """
        structure = []
        
        if current_depth >= max_depth:
            return structure
        
        try:
            for item in sorted(path.iterdir()):
                # Skip .git directory
                if item.name == ".git":
                    continue
                
                rel_path = item.relative_to(path)
                indent = "  " * current_depth
                
                if item.is_dir():
                    structure.append(f"{indent}{item.name}/")
                    # Recursively get subdirectory structure
                    sub_structure = self._get_directory_structure(item, max_depth, current_depth + 1)
                    structure.extend(sub_structure)
                else:
                    structure.append(f"{indent}{item.name}")
        except PermissionError:
            pass
        
        return structure
    
    def _read_key_files(self, path: Path) -> Dict[str, str]:
        """Read important files like README, package.json, requirements.txt, etc.
        
        Args:
            path: Repository path
            
        Returns:
            Dictionary mapping filename to content (truncated if too long)
        """
        key_files = {}
        important_files = [
            "README.md", "README.rst", "README.txt", "README",
            "package.json", "requirements.txt", "pyproject.toml",
            "Cargo.toml", "go.mod", "pom.xml", "build.gradle"
        ]
        
        for filename in important_files:
            file_path = path / filename
            if file_path.exists() and file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    # Truncate if too long
                    if len(content) > 5000:
                        content = content[:5000] + "\n... (truncated)"
                    key_files[filename] = content
                except Exception:
                    key_files[filename] = "[Error reading file]"
        
        return key_files
    
    def _get_repo_stats(self, path: Path) -> Dict[str, int]:
        """Get basic statistics about the repository.
        
        Args:
            path: Repository path
            
        Returns:
            Dictionary with file counts and sizes
        """
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size_bytes": 0
        }
        
        try:
            for item in path.rglob("*"):
                # Skip .git directory
                if ".git" in item.parts:
                    continue
                
                if item.is_file():
                    stats["total_files"] += 1
                    try:
                        stats["total_size_bytes"] += item.stat().st_size
                    except:
                        pass
                elif item.is_dir():
                    stats["total_dirs"] += 1
        except Exception:
            pass
        
        return stats
    
    def read_repo(self, repo_url: str, use_clone: bool = True) -> str:
        """Read and analyze a GitHub repository.
        
        Args:
            repo_url: The URL of the GitHub repository
            use_clone: If True, clone and analyze deeply. If False, use API only.
            
        Returns:
            A summary of the repository content
        """
        if use_clone:
            # Clone the repository
            clone_result = self.clone_repo(repo_url)
            
            if clone_result["status"] == "error":
                return f"Error: {clone_result['message']}"
            
            # Analyze the cloned repository
            analysis = self.analyze_cloned_repo(repo_url)
            
            if analysis["status"] == "error":
                return f"Error: {analysis['message']}"
            
            # Format the analysis into a readable summary
            summary = f"Repository: {analysis['owner']}/{analysis['repo']}\n"
            summary += f"Clone Path: {analysis['clone_path']}\n\n"
            
            summary += "Statistics:\n"
            summary += f"  - Files: {analysis['stats']['total_files']}\n"
            summary += f"  - Directories: {analysis['stats']['total_dirs']}\n"
            summary += f"  - Total Size: {analysis['stats']['total_size_bytes']:,} bytes\n\n"
            
            if analysis['key_files']:
                summary += "Key Files Found:\n"
                for filename in analysis['key_files'].keys():
                    summary += f"  - {filename}\n"
                summary += "\n"
            
            summary += "Directory Structure (top 3 levels):\n"
            structure_preview = analysis['structure'][:50]  # Limit to first 50 items
            summary += "\n".join(structure_preview)
            if len(analysis['structure']) > 50:
                summary += f"\n... and {len(analysis['structure']) - 50} more items"
            
            return summary
        else:
            # Use API-only approach (original implementation)
            try:
                owner, repo = self._parse_repo_url(repo_url)
                api_url = f"{self.api_base}/repos/{owner}/{repo}/contents"
                
                import requests
                response = requests.get(api_url)
                response.raise_for_status()
                
                contents = response.json()
                files = []
                for item in contents:
                    if item["type"] == "file":
                        files.append(item["name"])
                    elif item["type"] == "dir":
                        files.append(f"{item['name']}/")
                
                return f"Analyzed repo {owner}/{repo}. Found {len(files)} items: {', '.join(files[:10])}..."
                
            except Exception as e:
                return f"Error reading repo: {e}"
    
    def cleanup_repo(self, repo_url: str) -> Dict[str, any]:
        """Remove a cloned repository from the temp directory.
        
        Args:
            repo_url: The URL of the GitHub repository
            
        Returns:
            Dictionary with status and message
        """
        try:
            owner, repo = self._parse_repo_url(repo_url)
            clone_path = self.temp_dir / owner / repo
            
            if not clone_path.exists():
                return {
                    "status": "not_found",
                    "message": f"Repository not found at {clone_path}"
                }
            
            shutil.rmtree(clone_path)
            
            return {
                "status": "success",
                "message": f"Successfully removed {owner}/{repo}"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error cleaning up repo: {e}"}
    
    def cleanup_all(self) -> Dict[str, any]:
        """Remove all cloned repositories from the temp directory.
        
        Returns:
            Dictionary with status and message
        """
        try:
            if not self.temp_dir.exists():
                return {
                    "status": "success",
                    "message": "No repositories to clean up"
                }
            
            # Count repos before cleanup
            repo_count = sum(1 for _ in self.temp_dir.rglob("*/.git"))
            
            shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
            return {
                "status": "success",
                "message": f"Successfully removed {repo_count} repositories"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error cleaning up all repos: {e}"}
