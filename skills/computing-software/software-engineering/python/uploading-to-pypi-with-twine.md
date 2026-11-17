---
id: computing-software.software-engineering.python.uploading-to-pypi-with-twine
name: uploading-to-pypi-with-twine
category: computing-software
field: software-engineering
product: python
tags: [python, py-packaging-publish, twine-pypi-upload, twine, pypi, testpypi, api-token, twine-check, release]
level: practitioner
status: docs-checked
description: "Build, check and upload sdists and wheels to PyPI or TestPyPI with python -m build and twine, using API tokens, keyring or env credentials, and verifying the release."
sources: ["https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives", "https://twine.readthedocs.io/en/stable/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uploading to PyPI with twine

```
python3 -m pip install --upgrade build twine
python3 -m build                                  # creates dist/*.tar.gz and dist/*.whl
python3 -m twine check --strict dist/*            # --strict: fail on warnings

# Rehearse on TestPyPI first (separate account and token)
python3 -m twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps mypkg

python3 -m twine upload dist/*                    # real PyPI (default repository)
```

## Credentials
- Use a PyPI **API token**: when prompted, paste the token value including the `pypi-` prefix. TestPyPI and PyPI are separate instances, each needing its own account, verified email and token.
- Twine reads configuration from a `.pypirc` file (home directory, or `--config-file`) or from environment variables such as `TWINE_USERNAME`, `TWINE_PASSWORD` and `TWINE_REPOSITORY`; command-line options take precedence over environment variables. Use env vars on CI where creating `.pypirc` is inconvenient.
- Twine can also store credentials in keyring, e.g. `keyring set https://upload.pypi.org/legacy/ __token__`; `keyring --disable` turns it off if it causes unwanted prompts.
- Never commit tokens. For a supported CI/CD platform the packaging guide recommends Trusted Publishing instead of a long-lived API token.

## Rules
- `--skip-existing` continues uploading when a file already exists, which makes re-runs of partial uploads tolerable (check the twine docs for which repositories support it).
- The project name must not already be taken on PyPI; allowed characters are letters, numbers, `.`, `_` and `-`.
- Install from TestPyPI with `--index-url` and `--no-deps`: TestPyPI does not carry the same packages as PyPI, so dependency resolution there can fail or install something unexpected.
- TestPyPI is not permanent storage; it occasionally deletes packages and accounts.

## Gotchas
- Build into a clean `dist/`; `dist/*` uploads whatever is in the directory, including stale artifacts.

## Verify
- [ ] Install the published version in a fresh virtual environment and run an import smoke test.
- [ ] The PyPI project page lists the new version with all files.

## Checked
Date: 2026-11-03. Confirmed against the Python Packaging User Guide "Uploading the distribution archives" tutorial and the twine documentation: build, `twine check --strict`, `--repository testpypi`, `--index-url`/`--no-deps` install, token prompt with `pypi-` prefix, `.pypirc`, env variables and precedence, keyring commands, `--skip-existing`, Trusted Publishing recommendation. Removed as unconfirmed in the fetched pages: "passwords no longer work", mandatory 2FA, token scoping, once-only filename rule and yanking, 403 causes, 100 MB limit, `pip index versions`, `--extra-index-url` rehearsal, `rm -rf dist`, cibuildwheel and readme advice, pre-release behaviour.
Method: documentation only; no commands were run.
