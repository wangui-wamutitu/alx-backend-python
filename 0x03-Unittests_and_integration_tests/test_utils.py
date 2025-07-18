#!/usr/bin/env python3
"""Unit tests for access_nested_map"""
from parameterized import parameterized
import unittest
from typing import Mapping, Sequence, Any, Dict
from unittest.mock import patch, Mock
from utils import access_nested_map
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function.
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Mapping, path: Sequence, expected: Any
    ) -> None:
        """
        Test access_nested_map returns the correct value for valid paths.

        Args:
            nested_map (Mapping): The input map to test.
            path (Sequence): The path to access.
            expected (Any): The expected return value.
        """

        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(
        self, nested_map: Mapping, path: Sequence, expected_key: str
    ) -> None:
        """
        Test that KeyError is raised when path is invalid.

        Args:
            nested_map (Mapping): The input map to test.
            path (Sequence): The path to access.
            expected_key (str): The missing key that should appear in the exception.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """
    Test case for the get_json function.
    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock) -> None:
        """
        Test that get_json returns correct payload from mocked HTTP response.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests for memoize decorator
    """

    def test_memoize(self) -> None:
        """
        Test that memoize calls the method only once and returns the cached result.
        """
        class TestClass:
            """Class with a memoized property for testing."""

            def a_method(self) -> int:
                """Method that returns 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property that calls a_method."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
