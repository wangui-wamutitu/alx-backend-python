#!/usr/bin/env python3

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from typing import Dict
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
import requests


def get_json(url: str) -> Dict:
    """
    Get JSON from remote URL.

    Args:
        url (str): The URL to fetch JSON from.

    Returns:
        Dict: The parsed JSON response.
    """
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Client for GitHub organization data."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    def org(self) -> Dict:
        """Fetch organization data from GitHub."""
        url = self.ORG_URL.format(self.org_name)
        return get_json(url)

class TestGithubOrgClient(unittest.TestCase):
    """
    Unit Tests for GithubOrgClient.
    """

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org calls get_json once with the correct URL.

        Args:
            org_name (str): The name of the organization to test.
            mock_get_json: The mocked get_json function.
        """
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        result = client.org()

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the expected repos_url from mocked org.
        """
        payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("example")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns expected list of repo names and
        both get_json and _public_repos_url are called once.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_public_url:
            mock_public_url.return_value = "http://fake.url/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Assert the expected repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Assert internal calls
            mock_public_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake.url/repos")

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """
        Test that has_license correctly matches license keys.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


"""
Integration tests for GithubOrgClient using TEST_PAYLOAD fixtures.
"""


@parameterized_class(
    [
        {
            "org_payload": payload[0],
            "repos_payload": payload[1],
            "expected_repos": payload[2],
            "apache2_repos": payload[3],
        }
        for payload in TEST_PAYLOAD
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get to return fixture-based responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url == GithubOrgClient.ORG_URL.format("google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that GithubOrgClient.public_repos returns all repo names
        from the mocked fixture data.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that GithubOrgClient.public_repos filters repos by
        license='apache-2.0' from the mocked fixture data.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

if __name__ == "__main__":
    unittest.main()
