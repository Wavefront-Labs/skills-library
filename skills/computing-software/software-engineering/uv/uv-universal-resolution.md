---
id: computing-software.software-engineering.uv.uv-universal-resolution
name: uv-universal-resolution
category: computing-software
field: software-engineering
product: uv
tags: [uv, universal-resolution, resolution, environment-markers, required-environments, requires-python, lockfile]
level: practitioner
status: docs-checked
description: "Choose between uv platform-specific and universal resolution, and narrow or widen the solved platforms with environments and required-environments."
sources: [https://docs.astral.sh/uv/concepts/resolution/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv universal vs platform resolution

Goal: produce a resolution that works for every platform you support, and tune which platforms uv solves for.

## Method

- Project interface (`uv lock`, `uv sync`, `uv add`): `uv.lock` always comes from a universal resolution and is portable across OS, architecture and Python version. Platform-specific resolution is not available there.
- Pip interface: `uv pip compile` is platform-specific by default (like pip-tools). Add `--universal` to get a requirements file with markers saying which platform each dependency is for.
- Resolve for another platform: `uv pip compile --python-platform linux --python-version 3.10 requirements.in`. In platform-specific mode `--python-version` is the exact version, not a lower bound.
- Universal resolution must satisfy the whole `requires-python` range: the project's `requires-python` must be a subset of every dependency's. uv looks only at lower bounds, so `>=3.8, <4` is treated as `>=3.8`.
- A package can appear several times with different versions or URLs, selected by markers.

Limit the platforms solved with `environments` (entries must be disjoint, PEP 508 markers):

```toml
[tool.uv]
environments = [
    "sys_platform == 'darwin'",
    "sys_platform == 'linux'",
]
```

Require wheel coverage for packages with no source distribution (such as PyTorch) with `required-environments`; it expands what uv must support, while `environments` reduces it:

```toml
[tool.uv]
required-environments = [
    "sys_platform == 'darwin' and platform_machine == 'x86_64'"
]
```

macOS releases map to Darwin versions via `platform_release` (macOS 15 is Darwin 24, `'24.0.0'`); use `==` for baseline coverage, since `>=` can be satisfied by a wheel for a newer release only.

Preview: `minimum-libc-version = { glibc = "2.31" }` (with `preview-features = ["minimum-libc-version"]`) sets the oldest libc that `required-environments` must support; a `manylinux_2_17` wheel satisfies glibc 2.31, a `manylinux_2_34` wheel does not.

Common values: `sys_platform` is `'linux'`, `'darwin'`, `'win32'` (always win32 on Windows); `platform_machine` for ARM64 is `'aarch64'` (Linux), `'arm64'` (macOS), `'ARM64'` (Windows).

## Gotchas

- Universal resolution is often more constrained than platform-specific, since all markers are considered.
- Resolution fails if every version of a dependency needs a newer Python than your `requires-python` lower bound.

## Verify

Print marker values for the current machine: `uvx python -c "import sysconfig; print(sysconfig.get_config_vars())"`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/resolution). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
