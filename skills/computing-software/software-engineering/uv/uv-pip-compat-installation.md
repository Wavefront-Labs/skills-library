---
id: computing-software.software-engineering.uv.uv-pip-compat-installation
name: uv-pip-compat-installation
category: computing-software
field: software-engineering
product: uv
tags: [uv, pip-compatibility, pip-compat, user-install, only-binary, compile-bytecode, name-normalization]
level: advanced
status: docs-checked
description: "Install-time differences between uv pip and pip: venv default, no --user, --only-binary and --no-binary, bytecode, strictness, egg support, name normalization."
sources: [https://docs.astral.sh/uv/pip/compatibility/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv pip vs pip: installation differences

Goal: avoid surprises when swapping `pip install` for `uv pip install`.

## Method

- Virtual environments by default: `uv pip install` and `uv pip sync` use the active virtual environment or a `.venv` in the current or any parent directory, even if not activated. pip falls back to the global environment. To target others use `--python /path/to/python`, or `--system` (first interpreter on PATH, like pip).
- `--user` is unsupported and there is no fallback to the user install scheme when the target is not writable; use virtual environments.
- `--only-binary :all:` blocks source builds from registries in both tools. For direct URL dependencies uv enforces it and pip does not; exception: `uv pip install https://... --only-binary flask` builds the sdist if the package name cannot be inferred. Editable installs (`uv pip install -e . --only-binary :all:`) are allowed in both.
- `--no-binary`: uv refuses new wheels but reuses wheels already in its cache, and its resolver still reads metadata from wheels (pip does not).
- `manylinux_compatible` (PEP 600) is respected, but uv tests only the current glibc version and applies the result globally.
- Bytecode: unlike pip, uv does not compile `.pyc` files at install. Pass `--compile-bytecode` to `uv pip install` or `uv pip sync`, or set `UV_COMPILE_BYTECODE=1`. Recommended in Docker builds for startup time at the cost of build time. Without it you may see `SyntaxWarning` or `DeprecationWarning` messages that pip installs hide.
- Strictness: uv rejects things pip tolerates, such as HTML indexes with invalid URL fragments (PEP 503). Try a newer package version, then report to the maintainer.
- Wheels whose filename disagrees with the metadata version are rejected; override with `UV_SKIP_WHEEL_FILENAME_CHECK=1`.
- Registry auth: only `--keyring-provider subprocess` is supported (no `auto` or `import`), and keyring is not enabled by default.
- Legacy: no `.egg` support. Existing `.egg-info` and `.egg-link` installs are respected in resolution, shown by `uv pip list` and `uv pip freeze`, and removable with `uv pip uninstall`, but new ones cannot be installed.
- Names are normalized to PEP 503 form in output: `uv pip list` shows `docstring-parser` where `pip list` shows `docstring_parser`.
- Unsupported pip options include `--trusted-host` and `--user`.

## Verify

Compare `pip list` and `uv pip list` in the same environment: names such as `docstring_parser` appear as `docstring-parser` in uv.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (pip/compatibility). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
