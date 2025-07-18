#!/usr/bin/env python3
"""
This module contains unit and integration tests for the GithubOrgClient class,
including tests for memoization, mocking external requests, and parameterized
unit tests with license filtering.
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from typing import Dict
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: MagicMock) -> None:
        """
        Test that GithubOrgClient.org calls get_json once with the correct URL.

        Args:
            org_name (str): The name of the organization to test.
            mock_get_json (MagicMock): The mocked get_json function.
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

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("example")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        Test that public_repos returns expected list of repo names and
        both get_json and _public_repos_url are called once.

        Args:
            mock_get_json (MagicMock): The mocked get_json function.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_public_url:
            mock_public_url.return_value = "http://fake.url/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_public_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake.url/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """
        Test that has_license correctly matches license keys.

        Args:
            repo (Dict): The repository dictionary to check.
            license_key (str): The license key to compare.
            expected (bool): Expected result of the comparison.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient using fixture data.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Start patching requests.get to return fixture-based responses.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> Mock:
            mock_response = Mock()
            if url == GithubOrgClient.ORG_URL.format("google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stop the requests.get patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test that GithubOrgClient.public_repos returns all repo names
        from the mocked fixture data.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test that GithubOrgClient.public_repos filters repos by
        license='apache-2.0' from the mocked fixture data.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
