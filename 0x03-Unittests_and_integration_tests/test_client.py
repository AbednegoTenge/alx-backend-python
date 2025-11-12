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
        # Mock get_json to return the expected payload without making HTTP requests
        mock_get_json.return_value = expected_payload
        # Create a GithubOrgClient instance
        client = GithubOrgClient(org_name)
        # Access the org property (memoized, so it calls get_json)
        result = client.org
        # Build the expected URL that should be passed to get_json
        expected_url = f"https://api.github.com/orgs/{org_name}"
        # Verify get_json was called exactly once with the correct URL
        mock_get_json.assert_called_once_with(expected_url)
        # Verify the org property returns the expected payload
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url is the correct URL.
        """
        # Mock the org property to return a payload with repos_url
        # This avoids needing to mock get_json and the full org call chain
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            test_url = "https://api.github.com/orgs/google/repos"
            # Set up the mock org to return a dict with repos_url
            mock_org.return_value = {"repos_url": test_url}
            # Create a client instance
            client = GithubOrgClient("google")
            # Access _public_repos_url property which extracts repos_url from org
            result = client._public_repos_url
            # Verify that _public_repos_url correctly extracts repos_url from org
            self.assertEqual(result, mock_org.return_value["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names.
        """
        # Define test payload with repository data
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        # Mock get_json to return the test payload
        mock_get_json.return_value = test_payload

        # Mock _public_repos_url property to return a test URL
        # This is needed because repos_payload calls get_json with this URL
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            test_url = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = test_url
            # Create client instance
            client = GithubOrgClient("google")
            # Call public_repos which should extract names from the payload
            result = client.public_repos()

            # Build expected list of repository names
            expected = [repo["name"] for repo in test_payload]
            # Verify public_repos returns the correct list of repo names
            self.assertEqual(result, expected)
            # Verify get_json was called once with the URL from _public_repos_url
            mock_get_json.assert_called_once_with(
                mock_public_repos_url.return_value)
            # Verify _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected result.
        """
        # Test the static method has_license with different repo configurations
        # First case: repo has matching license key -> should return True
        # Second case: repo has different license key -> should return False
        result = GithubOrgClient.has_license(repo, license_key)
        # Verify the result matches the expected boolean value
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
