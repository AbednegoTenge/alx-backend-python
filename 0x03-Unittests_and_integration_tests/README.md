# 0x03-Unittests_and_integration_tests

This directory contains Python modules demonstrating various aspects of unit testing and integration testing, primarily focusing on testing a `GithubOrgClient`. It utilizes Python's `unittest` module, `parameterized` for data-driven tests, and `unittest.mock` for isolating components during testing.

## Table of Contents

- Project Description
- Concepts Covered
- Files
- How to Run Tests
- Requirements

## Project Description

The goal of this project is to implement and test a `GithubOrgClient` class that interacts with the GitHub API to retrieve information about an organization's repositories. The testing suite covers:

- **Unit Tests**: Verifying individual functions and methods in isolation.
- **Integration Tests**: Testing the interaction between different components, including mocked external API calls.
- **Parameterization**: Using `parameterized` to run tests with multiple sets of inputs.
- **Mocking**: Employing `unittest.mock.patch` to simulate external dependencies like network requests.
- **Memoization**: Testing a custom `memoize` decorator to ensure methods are called only once for the same inputs.

## Concepts Covered

- `unittest` module basics (`TestCase`, `assertEqual`, `assertRaises`)
- `parameterized` decorator for data-driven tests
- `unittest.mock.patch` for mocking functions and objects
- `unittest.mock.patch.object` for mocking methods on instances
- `wraps` argument in `patch.object`
- `memoize` decorator implementation and testing
- Understanding the difference between unit and integration tests

## Files

- `utils.py`: Contains utility functions and decorators (`access_nested_map`, `get_json`, `memoize`) that are used by the `GithubOrgClient` and tested independently.
- `client.py`: Implements the `GithubOrgClient` class, which interacts with the GitHub API.
- `test_utils.py`: Unit tests for the functions and decorators in `utils.py`.
- `fixtures.py`: Contains sample payload data used for mocking API responses in tests.

## How to Run Tests

To run all tests in this directory, navigate to the directory in your terminal and execute:

```bash
python -m unittest discover
```

Alternatively, you can run specific test files:

```bash
python -m unittest test_utils.py
```

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)
- `parameterized` library (`pip install parameterized`)