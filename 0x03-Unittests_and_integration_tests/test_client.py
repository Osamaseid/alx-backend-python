#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json  # Assuming get_json is in utils.py

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Setup the mock to return a predefined response
        expected_response = {"login": org_name}
        mock_get_json.return_value = expected_response

        # Create an instance of the client
        client = GithubOrgClient(org_name)

        # Assert that the method returns the correct response
        self.assertEqual(client.org, expected_response)

        # Assert that get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that GithubOrgClient._public_repos_url returns the expected value."""
        # Mocked payload for the org property
        mock_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
        mock_org.return_value = mock_payload

        # Create an instance of the client
        client = GithubOrgClient("test-org")

        # Assert that _public_repos_url returns the expected repos_url
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test-org/repos")

if __name__ == "__main__":
    unittest.main()
