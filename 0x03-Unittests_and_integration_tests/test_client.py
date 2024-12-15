#!/usr/bin/python3
import unittest
from unittest.mock import patch
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

if __name__ == "__main__":
    unittest.main()