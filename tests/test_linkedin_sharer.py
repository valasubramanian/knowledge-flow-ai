import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agent.tools.linkedin_sharer import LinkedInSharerTool

class TestLinkedInSharerTool(unittest.TestCase):

    def setUp(self):
        os.environ["LINKEDIN_ACCESS_TOKEN"] = "test_token"
        os.environ["LINKEDIN_USER_URN"] = "test_urn"
        self.tool = LinkedInSharerTool()

    @patch('requests.post')
    def test_post_article_summary_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "urn:li:share:12345"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.tool.post_article_summary(
            summary="Test summary",
            article_url="http://example.com/article"
        )

        self.assertIn("Successfully posted", result)
        self.assertIn("urn:li:share:12345", result)
        
        # Verify API call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['specificContent']['com.linkedin.ugc.ShareContent']['shareCommentary']['text'], "Test summary")
        self.assertEqual(kwargs['json']['specificContent']['com.linkedin.ugc.ShareContent']['media'][0]['originalUrl'], "http://example.com/article")

    @patch('requests.post')
    def test_post_article_summary_failure(self, mock_post):
        # Mock failure response
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("API Error")

        result = self.tool.post_article_summary(
            summary="Test summary",
            article_url="http://example.com/article"
        )

        self.assertIn("Failed to post", result)

if __name__ == '__main__':
    unittest.main()
