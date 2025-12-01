import os
import requests
import json
from typing import Dict, Any, Optional

class LinkedInSharerTool:
    """Tool for sharing content on LinkedIn."""

    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.api_url = "https://api.linkedin.com/v2/ugcPosts"
        self.user_info_url = "https://api.linkedin.com/v2/userinfo"

    def _get_user_urn(self) -> Optional[str]:
        """Fetches the authenticated user's URN from LinkedIn."""
        if not self.access_token:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        
        try:
            response = requests.get(self.user_info_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("sub")
        except requests.exceptions.RequestException:
            return None

    def post_article_summary(self, summary: str, article_url: str, visibility: str = "PUBLIC") -> str:
        """
        Posts a summary of an article to LinkedIn with a link.

        Args:
            summary: The text content of the post (the summary of the article).
            article_url: The URL of the deployed article.
            visibility: The visibility of the post. Defaults to "PUBLIC". 
                        Options: "PUBLIC", "CONNECTIONS".

        Returns:
            str: A message indicating success or failure, including the post ID if successful.
        """
        if not self.access_token:
            return "Error: LINKEDIN_ACCESS_TOKEN not found in environment variables."

        user_urn = self._get_user_urn()
        if not user_urn:
            return "Error: Failed to fetch LinkedIn User URN. Please check your access token."

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        post_data = {
            "author": f"urn:li:person:{user_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": summary
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": "Check out my new article!"
                            },
                            "originalUrl": article_url,
                            "title": {
                                "text": "New Article Deployed"
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=post_data)
            response.raise_for_status()
            data = response.json()
            return f"Successfully posted to LinkedIn. Post ID: {data.get('id')}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to post to LinkedIn: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f"\nResponse: {e.response.text}"
            return error_msg
