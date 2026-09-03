# Contributing

1. Create a virtual environment with Python 3.11 or newer.
2. Install the development tools: `python -m pip install -e '.[dev]'`.
3. Run `ruff check .`, `ruff format --check .`, and `pytest` before opening a pull request.
4. Add tests for behavior changes and use documentation-only example addresses from RFC 5737.

Do not include credentials, internal hostnames, device output, or production IP addresses in issues,
tests, examples, or commits.
