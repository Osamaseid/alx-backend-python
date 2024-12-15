#!/usr/bin/env python3
"""
Unit tests for utility functions in the utils module.
"""

import unittest
from unittest.mock import patch, Mock
from utils import memoize, access_nested_map, get_json
from parameterized import parameterized
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function.

    The access_nested_map function is expected to
    retrieve a value from a nested dictionary
    based on a provided path (sequence of keys).
    These tests verify its correct behavior
    and its ability to raise appropriate exceptions when keys are missing.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Mapping,
                               path: Sequence, expected: Any):
        """
        Test access_nested_map with various inputs to
        ensure it returns the correct values.

        :param nested_map: The input nested dictionary.
        :param path: A sequence of keys representing
        the path to the desired value.
        :param expected: The expected value to be
        returned by the function.
        """
        # Assert that the function returns the
        # expected value for the given nested_map and path
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence, expected_key: Any):
        """
        Test access_nested_map to ensure it raises
        a KeyError when a key is missing.

        :param nested_map: The input nested dictionary.
        :param path: A sequence of keys
        representing the path to the desired value.
        :param expected_key: The key expected
        to be missing, causing the KeyError.
        """
        # Use a context manager to catch the KeyError exception
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Assert that the exception message contains the expected missing key
        self.assertEqual(str(context.exception), repr(expected_key))


class TestGetJson(unittest.TestCase):
    """
    Unit tests for the get_json function.

    The get_json function is expected to
    perform an HTTP GET request to a specified URL
    and return the JSON payload from the response.
    These tests mock the requests.get
    method to ensure the function behaves
    correctly without making actual HTTP requests.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: dict):
        """
        Test get_json with mocked HTTP responses to
        ensure it returns the correct JSON payload.

        :param test_url: The URL to which the HTTP GET request is made.
        :param test_payload: The expected
        JSON payload to be returned by the function.
        """
        # Patch the 'requests.get' method in
        # the utils module to prevent actual HTTP requests
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = test_payload

            # Call the function being tested with the test URL
            result = get_json(test_url)

            # Assert that 'requests.get' was
            # called exactly once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Assert that the function returned the expected JSON payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Unit tests for the memoize decorator.

    The memoize decorator is expected to cache the
    result of a method call and return the cached
    result on subsequent calls, avoiding
    redundant computations. These tests verify that the
    decorator functions correctly by
    ensuring the decorated method is called only once.
    """

    def test_memoize(self):
        """
        Test that the memoize decorator caches method
        results and calls the original method only once.
        """
        class TestClass:
            def a_method(self) -> int:
                """
                A simple method that returns a fixed value.
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """
                A method decorated with @memoize that calls a_method.
                The result should be cached after the first call.
                """
                return self.a_method()

        # Create an instance of the TestClass
        test_obj = TestClass()

        # Patch the 'a_method' of the test_obj
        # instance to track its calls and return a fixed value
        with patch.object(test_obj, 'a_method') as mock_method:
            # Configure the mock method to return 42 when called
            mock_method.return_value = 42

            # First call to a_property;
            # should call a_method and cache the result
            result1 = test_obj.a_property

            # Second call to a_property; should return the
            # cached result without calling a_method again
            result2 = test_obj.a_property

            # Assert that a_method was called exactly
            # once during both property accesses
            mock_method.assert_called_once()

            # Assert that both calls to a_property
            # returned the expected cached value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == '__main__':
    # Run the unit tests when this script is executed directly
    unittest.main()
