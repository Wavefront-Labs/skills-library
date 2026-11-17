---
id: computing-software.software-engineering.python.pip-constraints-and-hash-checking
name: pip-constraints-and-hash-checking
category: computing-software
field: software-engineering
product: python
tags: [python, py-environments, pip-constraints-hashes, constraints-txt, require-hashes, reproducible-installs, supply-chain]
level: practitioner
status: docs-checked
description: "Make pip installs reproducible and tamper-evident with constraints files, pinned requirements, hash-checking mode (--require-hashes) and --only-binary."
sources: ["https://pip.pypa.io/en/stable/topics/secure-installs/", "https://pip.pypa.io/en/stable/user_guide/#constraints-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pip constraints and hash checking

## Requirements vs constraints
- A requirements file says **what to install**; a constraints file only controls **which version** of a requirement is installed, not whether it is installed. Constraints must have a name and cannot be editable.
```
python -m pip install -r requirements.txt -c constraints.txt
```
- Typical use: one constraints file for an organisation (it can also be served from a URL), so a fixed or patched version of a shared dependency is used everywhere it gets pulled in.
- Since pip 26.2, constraints (including `PIP_CONSTRAINT`) no longer affect isolated build environments; use `--build-constraint build-constraints.txt` for build dependencies.

## Hash-checking mode
```
FooProject == 1.2 \
    --hash=sha256:<hash-of-archive-1> \
    --hash=sha256:<hash-of-archive-2>
```
- `--hash` on any requirement turns hash-checking on globally ("all-or-nothing"); `--require-hashes` forces it, which suits deploy scripts and also prints the hashes of fetched packages to bootstrap your list.
- In this mode every requirement must be pinned (to a URL, filesystem path or `==`) and hashed, **including dependencies** that are not listed: an unlisted, unhashed dependency is an error.
- Give several `--hash` values per package when it ships wheels for several platforms or both binary and source distributions.
- sha256 is recommended; stronger hashlib algorithms are allowed, while md5, sha1 and sha224 are excluded.
- Hashes that PyPI publishes in download URLs only guard against corruption and do not satisfy `--require-hashes`.
- `--no-require-hashes` disables the automatic enforcement (needed to combine hashed requirements with local directories or VCS URLs); hashes are then checked only where given.
- `--only-binary :all:` disallows source distributions.
- Hash-checking also works with `pip download` and `pip wheel`.

## Gotchas
- Because hashes must match the file pip picks for the platform, list hashes for every wheel or sdist you may need.
- A pin without a hash still trusts the index at install time.

## Verify
- [ ] Install from the hashed file in a fresh virtual environment succeeds; changing one hash makes it fail.

## Checked
Date: 2026-11-03. Confirmed against pip's "Secure installs" topic and the user guide "Constraints Files" section (including the build-constraints note). Removed as unconfirmed in the fetched pages: pip-compile and pip-tools, uv commands and `uv.lock`, `--universal`, Dependabot/Renovate workflow, `pip check` and resolver backtracking remarks, environment-marker remarks, the sample `requests` pins and `urllib3<2`.
Method: documentation only; no commands were run.
