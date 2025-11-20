import os
import requests
import base64

class GitHubReader:
    def __init__(self):
        self.name = "github_reader"
        self.api_base = "https://api.github.com"
    
    def read_repo(self, repo_url: str):
        """Reads and analyzes a GitHub repository.
        
        Args:
            repo_url: The URL of the GitHub repository (e.g., https://github.com/user/repo).
            
        Returns:
            A summary of the repository content.
        """
        try:
            # Extract owner and repo from URL
            parts = repo_url.rstrip("/").split("/")
            if len(parts) < 2:
                return "Invalid GitHub URL."
            owner, repo = parts[-2], parts[-1]
            
            # Fetch repo details
            api_url = f"{self.api_base}/repos/{owner}/{repo}/contents"
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
