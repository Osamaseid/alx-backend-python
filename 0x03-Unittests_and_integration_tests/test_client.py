#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from client import GithubOrgClient  # Adjust the import based on your project structure


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method of GithubOrgClient.

        Mocks the get_json method and the _public_repos_url attribute
        to verify that the public_repos method returns the expected
        list of repository names and that the mocks are called correctly.
        """
        # Sample payload to return from the mocked get_json method
        mock_payload = [
            {'id': 1, 'name': 'Repo1'},
            {'id': 2, 'name': 'Repo2'},
        ]
        mock_get_json.return_value = mock_payload

        # Mock the _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url', new_callable=MagicMock) as mock_url:
            mock_url.return_value = 'https://api.github.com/orgs/test_org/repos'

            client = GithubOrgClient('test_org')
            repos = client.public_repos()

            # Assert the returned repos match the expected payload
            self.assertEqual(repos, ['Repo1', 'Repo2'])

            # Assert that get_json was called once
            mock_get_json.assert_called_once()
            # Assert that the mocked URL property was accessed
            mock_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()