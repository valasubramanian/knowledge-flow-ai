"""Tool for creating articles with human-in-the-loop workflow.

This tool helps create well-structured articles based on source information
from GitHub repositories, blog posts, or research topics.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ArticleCreatorTool:
    """Tool for creating articles with iterative refinement."""
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize the Article Creator tool.
        
        Args:
            project_root: Root directory of the project. If None, uses current working directory.
        """
        self.name = "article_creator"
        
        # Set up directory for article drafts
        if project_root is None:
            project_root = os.getcwd()
        self.drafts_dir = Path(project_root) / "temp" / "article_drafts"
        self.drafts_dir.mkdir(parents=True, exist_ok=True)
    
    def create_article_structure(self, topic: str, outline: str, source_info: str = "") -> str:
        """Create an article structure/outline for user approval.
        
        This is the first step in the human-in-the-loop workflow.
        The agent should present this structure to the user for approval.
        
        Args:
            topic: The main topic/title of the article
            outline: Proposed outline with sections and subsections
            source_info: Brief description of source materials used
            
        Returns:
            String with formatted structure for user review
        """
        try:
            structure = {
                "topic": topic,
                "outline": outline,
                "source_info": source_info,
                "created_at": datetime.now().isoformat(),
                "status": "structure_proposed"
            }
            
            # Save structure for reference
            structure_id = self._generate_id(topic)
            structure_file = self.drafts_dir / f"{structure_id}_structure.json"
            
            with open(structure_file, 'w') as f:
                json.dump(structure, f, indent=2)
            
            formatted_output = f"""
Article Structure Created
========================

Topic: {topic}

Outline:
{outline}

Source Information:
{source_info}

Structure ID: {structure_id}
Saved to: {structure_file}

Please review this structure. Once approved, I can proceed with generating the full article content.
"""
            return formatted_output
            
        except Exception as e:
            return f"Error creating article structure: {str(e)}"
    
    def generate_article_content(
        self, 
        structure_id: str, 
        content: str,
        metadata: str = ""
    ) -> str:
        """Generate article content based on approved structure.
        
        Args:
            structure_id: ID of the approved structure
            content: The full article content in markdown format
            metadata: Optional metadata as JSON string (e.g., '{"author": "John", "tags": ["tech"]}')
            
        Returns:
            String with article preview and save location
        """
        try:
            # Load the structure
            structure_file = self.drafts_dir / f"{structure_id}_structure.json"
            if not structure_file.exists():
                return f"Error: Structure ID '{structure_id}' not found. Please create structure first."
            
            with open(structure_file, 'r') as f:
                structure = json.load(f)
            
            # Prepare article with metadata
            # Parse metadata from JSON string if provided
            if metadata:
                try:
                    metadata_dict = json.loads(metadata)
                except json.JSONDecodeError:
                    metadata_dict = {}
            else:
                metadata_dict = {}
            
            article_data = {
                "topic": structure["topic"],
                "content": content,
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "source_info": structure.get("source_info", ""),
                    **metadata_dict
                },
                "status": "draft_generated"
            }
            
            # Save article draft
            article_file = self.drafts_dir / f"{structure_id}_article.json"
            with open(article_file, 'w') as f:
                json.dump(article_data, f, indent=2)
            
            # Also save as markdown for easy preview
            md_file = self.drafts_dir / f"{structure_id}_article.md"
            with open(md_file, 'w') as f:
                # Write frontmatter if metadata exists
                if metadata_dict:
                    f.write("---\n")
                    f.write(f"title: {structure['topic']}\n")
                    for key, value in metadata_dict.items():
                        f.write(f"{key}: {value}\n")
                    f.write("---\n\n")
                
                f.write(f"# {structure['topic']}\n\n")
                f.write(content)
            
            preview = content[:500] + "..." if len(content) > 500 else content
            
            return f"""
Article Content Generated
=========================

Topic: {structure['topic']}

Preview:
{preview}

Full article saved to:
- JSON: {article_file}
- Markdown: {md_file}

Article ID: {structure_id}

You can now review the article and request refinements, or proceed to deployment.
"""
            
        except Exception as e:
            return f"Error generating article content: {str(e)}"
    
    def refine_article_section(
        self, 
        structure_id: str, 
        section_name: str, 
        refined_content: str
    ) -> str:
        """Refine a specific section of the article based on user feedback.
        
        Args:
            structure_id: ID of the article to refine
            section_name: Name of the section to refine
            refined_content: The refined content for this section
            
        Returns:
            String confirming the refinement
        """
        try:
            article_file = self.drafts_dir / f"{structure_id}_article.json"
            if not article_file.exists():
                return f"Error: Article ID '{structure_id}' not found."
            
            with open(article_file, 'r') as f:
                article_data = json.load(f)
            
            # Update the content (simple replacement for now)
            # In a more sophisticated version, we'd parse sections
            article_data["content"] = article_data["content"].replace(
                section_name, 
                refined_content
            )
            article_data["metadata"]["last_refined"] = datetime.now().isoformat()
            article_data["status"] = "refined"
            
            # Save updated article
            with open(article_file, 'w') as f:
                json.dump(article_data, f, indent=2)
            
            # Update markdown file
            md_file = self.drafts_dir / f"{structure_id}_article.md"
            with open(md_file, 'w') as f:
                metadata = article_data.get("metadata", {})
                if metadata:
                    f.write("---\n")
                    f.write(f"title: {article_data['topic']}\n")
                    for key, value in metadata.items():
                        if key not in ["created_at", "source_info", "last_refined"]:
                            f.write(f"{key}: {value}\n")
                    f.write("---\n\n")
                
                f.write(f"# {article_data['topic']}\n\n")
                f.write(article_data["content"])
            
            return f"""
Section Refined
===============

Article ID: {structure_id}
Section: {section_name}

Updated article saved to: {md_file}

The article has been refined. You can request more refinements or proceed to deployment.
"""
            
        except Exception as e:
            return f"Error refining article section: {str(e)}"
    
    def get_article_for_deployment(self, structure_id: str) -> Dict:
        """Get article data ready for deployment.
        
        Args:
            structure_id: ID of the article to deploy
            
        Returns:
            Dictionary with article content and metadata, or error message
        """
        try:
            article_file = self.drafts_dir / f"{structure_id}_article.json"
            if not article_file.exists():
                return {"error": f"Article ID '{structure_id}' not found."}
            
            with open(article_file, 'r') as f:
                article_data = json.load(f)
            
            # Also get the markdown file path
            md_file = self.drafts_dir / f"{structure_id}_article.md"
            
            return {
                "topic": article_data["topic"],
                "content": article_data["content"],
                "metadata": article_data.get("metadata", {}),
                "markdown_file": str(md_file),
                "status": "ready_for_deployment"
            }
            
        except Exception as e:
            return {"error": f"Error retrieving article: {str(e)}"}
    
    def list_articles(self) -> str:
        """List all article drafts.
        
        Returns:
            String with list of all articles
        """
        try:
            articles = []
            for file in self.drafts_dir.glob("*_article.json"):
                with open(file, 'r') as f:
                    data = json.load(f)
                    structure_id = file.stem.replace("_article", "")
                    articles.append({
                        "id": structure_id,
                        "topic": data["topic"],
                        "status": data.get("status", "unknown"),
                        "created": data.get("metadata", {}).get("created_at", "unknown")
                    })
            
            if not articles:
                return "No article drafts found."
            
            output = "Article Drafts\n==============\n\n"
            for article in articles:
                output += f"ID: {article['id']}\n"
                output += f"Topic: {article['topic']}\n"
                output += f"Status: {article['status']}\n"
                output += f"Created: {article['created']}\n"
                output += "-" * 50 + "\n"
            
            return output
            
        except Exception as e:
            return f"Error listing articles: {str(e)}"
    
    def _generate_id(self, topic: str) -> str:
        """Generate a unique ID for an article based on topic and timestamp.
        
        Args:
            topic: The article topic
            
        Returns:
            Unique identifier string
        """
        # Create a slug from the topic
        slug = topic.lower().replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        slug = slug[:50]  # Limit length
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        return f"{slug}-{timestamp}"
