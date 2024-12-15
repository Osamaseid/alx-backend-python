#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient  # Adjust the import based on your project structure
from fixtures import org_payload, repos_payload, expected_repos  # Adjust as necessary

@parameterized_class(("org_payload", "repos_payload", "expected_repos"), [
    (org_payload, repos_payload, expected_repos),
    # You can add more fixtures here if needed
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up the patcher for requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define the side effects for different URLs
        cls.mock_get.side_effect = cls._mock_requests_get

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    @classmethod
    def _mock_requests_get(cls, url):
        """Return mock responses based on the URL requested."""
        if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
            return MockResponse(cls.org_payload)
        elif url == f"https://api.github.com/orgs/{cls.org_payload['login']}/repos":
            return MockResponse(cls.repos_payload)
        return MockResponse({})  # Return an empty response for unexpected URLs

    def test_public_repos(self):
        """Test the public_repos method of GithubOrgClient."""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos()

        # Assert the returned repos match the expected payload
        self.assertEqual(repos, self.expected_repos)

class MockResponse:
    """Mock response class for requests.get."""
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        """Return the mock JSON data."""
        return self.json_data

if __name__ == '__main__':
    unittest.main()