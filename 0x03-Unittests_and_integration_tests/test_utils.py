#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict, Callable
from unittest.mock import patch, Mock
from functools import wraps
import requests

"""
Unit tests for the access_nested_map function.
"""


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map


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
        self.assertEqual(str(context.exception), f"'{expected_key}'")


"""
Unit tests for the get_json function.
"""


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
    @patch("requests.get")
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock) -> None:
        """
        Test that get_json returns correct payload from mocked HTTP response.

        Args:
            test_url (str): The URL being requested.
            test_payload (Dict): The expected JSON payload to be returned.
            mock_get (Mock): The mocked requests.get function.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method.
    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            print("a_method called")
            return 42
    >>> my_object = MyClass()
    >>> my_object.a_method
    a_method called
    42
    >>> my_object.a_method
    42
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        """ "memoized wraps"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)


class TestMemoize(unittest.TestCase):
    """
    Test case for the memoize decorator.
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
