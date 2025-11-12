#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import *
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://exmaple.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, payload, mock_get):
        mock_get.return_value.json.return_value = payload
        result = get_json(url)
        self.assertEqual(result, payload)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):

    def test_memoize(self):

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, 'a_method',
                          wraps=test_obj.a_method) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
