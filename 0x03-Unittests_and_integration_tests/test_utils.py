#!/usr/bin/env python3
"""Unit tests for utils module.
"""

import unittest
from parameterized import parameterized
from utils import *
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid paths.
        """
        # Test that access_nested_map correctly navigates nested dictionaries
        # using the provided path and returns the expected value
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths.
        """
        # Test that access_nested_map raises KeyError when trying to access
        # a non-existent key in the nested map
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Verify that the exception message contains the missing key
        self.assertEqual(context.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function.
    """

    @parameterized.expand([
        ("http://exmaple.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, payload, mock_get):
        """Test get_json returns JSON payload from URL.
        """
        # Mock the requests.get call to avoid making actual HTTP requests
        # Set up the mock to return a response with a json() method
        mock_get.return_value.json.return_value = payload
        # Call get_json with the test URL
        result = get_json(url)
        # Verify that get_json returns the expected payload
        self.assertEqual(result, payload)
        # Verify that requests.get was called exactly once with the correct URL
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator.
    """

    def test_memoize(self):
        """Test memoize decorator caches method results.
        """

        class TestClass:
            """Test class for memoize testing.
            """
            def a_method(self):
                """Return a test value.
                """
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method.
                """
                return self.a_method()

        # Create a test instance
        test_obj = TestClass()
        # Mock a_method to track how many times it's called
        # Using wraps to preserve the original method behavior
        with patch.object(TestClass, 'a_method',
                          wraps=test_obj.a_method) as mock_method:
            # Access the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            # Verify both calls return the same value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            # Verify that a_method was only called once due to memoization
            # (the second access should use the cached value)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
