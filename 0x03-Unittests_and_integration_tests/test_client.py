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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns the correct list of repos."""
        # Setup the mock payload for get_json
        expected_repos = ["repo1", "repo2", "repo3"]
        mock_get_json.return_value = [{"name": name} for name in expected_repos]

        # Mock _public_repos_url with a context manager
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"

            # Create an instance of the client
            client = GithubOrgClient("test-org")

            # Assert that public_repos returns the expected list of repos
            self.assertEqual(client.public_repos(), expected_repos)

            # Assert that _public_repos_url and get_json were called once
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that GithubOrgClient.has_license works as expected."""
        # Create an instance of the client
        client = GithubOrgClient("test-org")

        # Assert that has_license returns the expected value
        self.assertEqual(client.has_license(repo, license_key), expected)

if __name__ == "__main__":
    unittest.main()
