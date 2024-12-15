#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up for integration tests."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Define a side_effect for the mock
        def get_json_side_effect(url):
            if url == "https://api.github.com/orgs/test-org":
                return cls.org_payload
            if url == "https://api.github.com/orgs/test-org/repos":
                return cls.repos_payload
            return None

        # Set the side_effect for json() calls on the mock
        cls.mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down the mock patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filtering."""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
