"""Tool for deploying articles to GitHub Pages.

This tool handles the deployment of articles to a GitHub Pages repository
using the GitHub API and git operations.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict
from datetime import datetime
import json
import re


class GitHubPagesDeployerTool:
    """Tool for deploying articles to GitHub Pages."""
    
    def __init__(self, project_root: str = ""):
        """Initialize the GitHub Pages Deployer tool.
        
        Args:
            project_root: Root directory of the project. If empty, uses current working directory.
        """
        self.name = "github_pages_deployer"
        
        # Set up temp directory for git operations
        if not project_root:
            project_root = os.getcwd()
        self.temp_dir = Path(project_root) / "temp" / "github_pages"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Get GitHub token from environment
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            print("Warning: GITHUB_TOKEN not found in environment variables.")
    
    def deploy_article(
        self,
        article_content: str,
        title: str,
        metadata: Dict[str, str] = {},
        repo_url: str = "",
        repo_owner: str = "",
        repo_name: str = ""
    ) -> str:
        """Deploy an article to GitHub Pages.
        
        This method:
        1. Clones or updates the GitHub Pages repository
        2. Creates a Jekyll-compatible post file in _posts/ directory
        3. Commits and pushes the changes
        4. Returns the GitHub Pages URL
        
        Args:
            article_content: The article content in markdown format
            title: The article title
            metadata: Optional metadata (author, tags, categories, date, etc.)
            repo_url: Full GitHub repository URL (e.g., https://github.com/user/repo)
            repo_owner: GitHub repository owner (alternative to repo_url)
            repo_name: GitHub repository name (alternative to repo_url)
            
        Returns:
            String with deployment status and URL
        """
        try:
            if not self.github_token:
                return "Error: GITHUB_TOKEN not set. Please set the GITHUB_TOKEN environment variable."
            
            # Parse repository information
            if repo_url:
                owner, name = self._parse_repo_url(repo_url)
            elif repo_owner and repo_name:
                owner, name = repo_owner, repo_name
            else:
                return "Error: Please provide either repo_url or both repo_owner and repo_name."
            
            # Clone or update repository
            repo_path = self.temp_dir / owner / name
            if repo_path.exists():
                # Pull latest changes
                result = subprocess.run(
                    ["git", "-C", str(repo_path), "pull"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    return f"Error pulling repository: {result.stderr}"
            else:
                # Clone repository
                repo_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Use token authentication
                auth_url = f"https://{self.github_token}@github.com/{owner}/{name}.git"
                result = subprocess.run(
                    ["git", "clone", auth_url, str(repo_path)],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    return f"Error cloning repository: {result.stderr}"
            
            # Create _posts directory if it doesn't exist
            posts_dir = repo_path / "_posts"
            posts_dir.mkdir(exist_ok=True)
            
            # Generate Jekyll-compatible filename: YYYY-MM-DD-title.md
            date_str = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
            if isinstance(date_str, str) and len(date_str) > 10:
                # Extract just the date part if it's a full ISO timestamp
                date_str = date_str[:10]
            
            # Create slug from title
            slug = self._create_slug(title)
            filename = f"{date_str}-{slug}.md"
            file_path = posts_dir / filename
            
            # Create article with Jekyll frontmatter
            with open(file_path, 'w') as f:
                # Write YAML frontmatter
                f.write("---\n")
                f.write(f"layout: post\n")
                f.write(f"title: \"{title}\"\n")
                
                # Add metadata
                if "author" in metadata:
                    f.write(f"author: {metadata['author']}\n")
                if "date" in metadata:
                    f.write(f"date: {metadata['date']}\n")
                if "categories" in metadata:
                    categories = metadata['categories']
                    if isinstance(categories, list):
                        f.write(f"categories: {' '.join(categories)}\n")
                    else:
                        f.write(f"categories: {categories}\n")
                if "tags" in metadata:
                    tags = metadata['tags']
                    if isinstance(tags, list):
                        f.write(f"tags: [{', '.join(tags)}]\n")
                    else:
                        f.write(f"tags: [{tags}]\n")
                if "description" in metadata:
                    f.write(f"description: \"{metadata['description']}\"\n")
                
                f.write("---\n\n")
                
                # Write article content
                f.write(article_content)
            
            # Git add, commit, and push
            subprocess.run(
                ["git", "-C", str(repo_path), "add", str(file_path)],
                check=True,
                capture_output=True
            )
            
            commit_message = f"Add article: {title}"
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "-m", commit_message],
                check=True,
                capture_output=True,
                text=True
            )
            
            subprocess.run(
                ["git", "-C", str(repo_path), "push"],
                check=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Generate GitHub Pages URL
            # Standard format: https://username.github.io/repo-name/YYYY/MM/DD/slug.html
            year, month, day = date_str.split("-")
            pages_url = f"https://{owner}.github.io/{name}/{year}/{month}/{day}/{slug}.html"
            
            return f"""
Article Deployed Successfully!
==============================

Repository: {owner}/{name}
File: _posts/{filename}
Commit: {commit_message}

GitHub Pages URL: {pages_url}

Note: It may take a few minutes for GitHub Pages to build and publish your article.
You can check the deployment status in your repository's Actions tab.

Direct file URL: https://github.com/{owner}/{name}/blob/main/_posts/{filename}
"""
            
        except subprocess.TimeoutExpired:
            return "Error: Git operation timed out."
        except subprocess.CalledProcessError as e:
            return f"Error during git operation: {e.stderr if e.stderr else str(e)}"
        except Exception as e:
            return f"Error deploying article: {str(e)}"
    
    def validate_deployment(self, url: str) -> str:
        """Validate that a deployed article is accessible.
        
        Args:
            url: The GitHub Pages URL to validate
            
        Returns:
            String with validation status
        """
        try:
            import urllib.request
            
            # Try to fetch the URL
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                
                if status_code == 200:
                    return f"✓ Article is accessible at: {url}"
                else:
                    return f"Warning: Received status code {status_code} for {url}"
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return f"Article not yet published. GitHub Pages may still be building. Please wait a few minutes and try again.\nURL: {url}"
            else:
                return f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            return f"Could not validate deployment: {str(e)}\nURL: {url}\n\nNote: The article may still be deploying. Check the repository's Actions tab."
    
    def _parse_repo_url(self, repo_url: str) -> tuple:
        """Parse GitHub repository URL to extract owner and repo name.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo_name)
        """
        # Remove .git suffix if present
        repo_url = repo_url.rstrip("/").replace(".git", "")
        
        # Extract from various URL formats
        patterns = [
            r"github\.com[:/]([^/]+)/([^/]+)",
            r"([^/]+)/([^/]+)$"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                return match.group(1), match.group(2)
        
        raise ValueError(f"Could not parse repository URL: {repo_url}")
    
    def _create_slug(self, title: str) -> str:
        """Create a URL-friendly slug from a title.
        
        Args:
            title: The article title
            
        Returns:
            URL-friendly slug
        """
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().replace(" ", "-")
        
        # Remove special characters
        slug = re.sub(r"[^a-z0-9-]", "", slug)
        
        # Remove multiple consecutive hyphens
        slug = re.sub(r"-+", "-", slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip("-")
        
        return slug
