---
id: computing-software.software-engineering.python.version-compatibility-shims-and-backports
name: version-compatibility-shims-and-backports
category: computing-software
field: software-engineering
product: python
tags: [python, py-versions, py-ver-compat, version-compat-shims, sys-version-info, typing-extensions, backports, requires-python]
level: practitioner
status: docs-checked
description: "Support several Python versions cleanly: sys.version_info gates, typing_extensions backports, one compat module and the requires-python metadata field."
sources: ["https://docs.python.org/3/library/sys.html#sys.version_info", "https://typing-extensions.readthedocs.io/en/latest/", "https://packaging.python.org/en/latest/specifications/pyproject-toml/#requires-python"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Version compatibility shims and backports

## Declare support
```toml
[project]
requires-python = ">=3.10"
```
`requires-python` in `pyproject.toml` maps to the core metadata field `Requires-Python`. Pick the minimum deliberately and keep CI covering every version you claim.

## One compat module
```python
# _compat.py: the only file that branches on versions
import sys
if sys.version_info >= (3, 11):
    from typing import Self, assert_never
else:
    from typing_extensions import Self, assert_never
```
- `sys.version_info` is a tuple of major, minor, micro, releaselevel and serial, so compare it with tuples such as `(3, 11)`. The docs say not to extract version information from the `sys.version` string.
- `typing_extensions` backports typing features: `Self` entered `typing` in 3.11 and `assert_never` in 3.11 (the table in its docs lists the release that first included each).
- The typing_extensions docs advise checking both the `typing` and `typing_extensions` versions of an object, since later releases may re-export a separate version to backport a fix.
- Keep all version branching in one module so the rest of the code imports names from it.

## Gotchas
- Behaviour changes without API changes need tests per supported version, not import shims.
- Removing support for an old version is a breaking-ish change for downstream users; update `requires-python` together with CI rather than only deleting CI jobs.

## Verify
- [ ] The package installs and imports in clean environments on the minimum and maximum supported Python.

## Checked
Date: 2026-11-03. Confirmed against `sys.version_info` docs, the typing_extensions documentation (Self and assert_never rows, advice on checking both modules) and the pyproject.toml specification (`requires-python` and `Requires-Python`). Removed as unconfirmed in the fetched pages: classifier and dependency-marker examples, release-schedule and SPEC 0/NEP 29 policy claims, backport package list beyond typing_extensions, pyupgrade/ruff/uv/tox/CI-matrix advice, `datetime.utcnow` remark, `from __future__ import annotations` and syntax-gating claims, type-checker flags.
Method: documentation only; no commands were run.
