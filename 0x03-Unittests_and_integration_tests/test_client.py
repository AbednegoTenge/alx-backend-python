#!/usr/bin/env python3
"""Test cases for GithubOrgClient class.
"""

import unittest
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD


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
        # Mock get_json to return the expected payload without making HTTP
        # requests
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
            # Access _public_repos_url property which extracts repos_url
            # from org
            result = client._public_repos_url
            # Verify that _public_repos_url correctly extracts repos_url from
            #  org
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
            # Verify get_json was called once with the URL from
            # _public_repos_url
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

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test filtering repos by apache-2.0 license."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ]

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_prop:
            mock_prop.return_value = "test_url"

            client = GithubOrgClient("test_org")
            result = client.public_repos(license="apache-2.0")

            self.assertEqual(result, ["repo1", "repo3"])
            mock_prop.assert_called_once()
            mock_get_json.assert_called_once_with("test_url")

@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the integration tests.
        """
        # Patch requests.get at the class level to mock external HTTP requests
        # This patcher will persist across all test methods in this class
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        # Set up side_effect to return different payloads based on URL
        # The side_effect function will determine which fixture to return
        cls.mock_get.side_effect = cls.side_effect

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures after all tests.
        """
        # Stop the patcher to restore the original requests.get
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repos.
        """
        # Create a GithubOrgClient instance with "google"
        # The org name is extracted from the repos_url in org_payload
        repos_url = self.org_payload.get("repos_url")
        org_name = repos_url.split("/")[-2] if repos_url else "google"
        client = GithubOrgClient(org_name)
        # Call public_repos without license filter
        result = client.public_repos()
        # Verify that public_repos returns all expected repos
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos with license filter returns apache-2.0 repos.
        """
        # Create a GithubOrgClient instance with "google"
        repos_url = self.org_payload.get("repos_url")
        org_name = repos_url.split("/")[-2] if repos_url else "google"
        client = GithubOrgClient(org_name)
        # Call public_repos with apache-2.0 license filter
        result = client.public_repos(license="apache-2.0")
        # Verify that public_repos returns only apache-2.0 licensed repos
        self.assertEqual(result, self.apache2_repos)

    @classmethod
    def side_effect(cls, url):
        """Side effect function that returns different payloads based on URL.
        This function is called by the mocked requests.get to determine
        which payload to return based on the requested URL.

        Args:
            url: The URL being requested

        Returns:
            dict or list: The payload to return based on the URL
        """
        # Create a mock response object that has a json() method
        # This simulates the requests.get(url).json() call in get_json
        class MockResponse:
            def __init__(self, payload):
                """Init method of MockResponse"""
                self._payload = payload

            def json(self):
                return self._payload

        # Return org payload when requesting org URL
        # Extract org name from repos_url in org_payload
        # The repos_url format is: "https://api.github.com/orgs/{org}/repos"
        repos_url = cls.org_payload.get("repos_url")
        if repos_url:
            # Extract org name from repos_url
            org_url = repos_url.replace("/repos", "")
            if url == org_url:
                return MockResponse(cls.org_payload)
            # Return repos payload when requesting repos URL
            if url == repos_url:
                return MockResponse(cls.repos_payload)
        # Return empty dict for other URLs
        return MockResponse({})


if __name__ == "__main__":
    unittest.main()
