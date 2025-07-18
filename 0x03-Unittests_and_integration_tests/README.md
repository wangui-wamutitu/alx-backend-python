# GithubOrgClient & Utils Testing

This project includes **unit tests** and **integration tests** for:
- `GithubOrgClient` (interacting with GitHub API)
- `utils.py` helper functions (`access_nested_map`, `get_json`, `memoize`)

All tests avoid real HTTP calls using mocks. They are written using `unittest`, `mock`, and `parameterized`.

---

## Purpose

To ensure the correctness of both isolated logic (unit tests) and full workflows (integration tests), especially when dealing with nested data, API calls, and caching.

---

## Unit Tests

### `utils.py`

| Function | Tested Behavior |
|----------|-----------------|
| `access_nested_map()` | Traverses nested maps safely. Tests valid and invalid paths. |
| `get_json()` | Mocked API call. Ensures correct JSON returned from a URL. |
| `memoize()` | Ensures the memoized function is only called once. Uses `@mock.patch` |

---

### `client.py` (GithubOrgClient)

| Method | Tested Behavior |
|--------|-----------------|
| `org` | Fetches organization data from GitHub. Mocked `get_json`. |
| `_public_repos_url` | Returns the `repos_url` from `.org`. |
| `public_repos()` | Returns list of repo names from GitHub response. |
| `has_license()` | Filters repos by license key. Parameterized test cases. |

---

## Integration Tests

These test the actual behavior of multiple connected methods using fixture data from `fixtures.py`.

| Test | Description |
|------|-------------|
| `test_public_repos()` | Returns all repos from a given GitHub org |
| `test_public_repos_with_license()` | Filters repos by `apache-2.0` license |
| Uses `@parameterized_class` | Each test runs with fixture values |
| Uses `patch("requests.get")` | Mocks GitHub API response with `side_effect` |

---

## Running the Tests

```bash
python3 test_utils.py
python3 test_client.py

```
Or run all tests at once
```bash
python3 -m unittest discover
````