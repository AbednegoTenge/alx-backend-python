#!/usr/bin/env python3
"""Test cases for GithubOrgClient class.
"""

import unittest
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class.
    """
    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that org method returns correct payload.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    
    def test_public_repos_url(self):
        """Test that _public_repos_url is the correct URL.
        """

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(result, mock_org.return_value["repos_url"])

    @parameterized.expand([
        ("google", [
            {"name": "repo1"},
            {"name": "repo2"},
        ]),
        ("abc", [
            {"name": "projectX"},
            {"name": "projectY"},
        ]),
    ])
    @patch("client.get_json")
    def test_public_repos(self, org_name, fake_repos, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""

        # Mock get_json to return fake repository data
        mock_get_json.return_value = fake_repos

        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = f"https://api.github.com/orgs/{org_name}/repos"

            client = GithubOrgClient(org_name)
            result = client.public_repos()

            # Expected list of repository names
            expected = [repo["name"] for repo in fake_repos]

            # Assertions
            self.assertEqual(result, expected)
            mock_get_json.assert_called_once_with(mock_url.return_value)
            mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()