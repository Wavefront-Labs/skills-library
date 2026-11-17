---
id: computing-software.software-engineering.uv.uv-docker-optimization
name: uv-docker-optimization
category: computing-software
field: software-engineering
product: uv
tags: [uv, docker, docker-integration, cache-mount, bytecode, no-editable, multi-stage, attestation]
level: practitioner
status: docs-checked
description: "Speed up and shrink uv Docker builds with layers, cache mounts, bytecode compilation, non-editable multi-stage installs and image attestation checks."
sources: [https://docs.astral.sh/uv/guides/integration/docker/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv Docker build optimization

Goal: fast, small, verifiable uv images.

## Method

### Bytecode

```dockerfile
RUN uv python install --compile-bytecode
RUN uv sync --compile-bytecode
```

Or `ENV UV_COMPILE_BYTECODE=1` for every command. uv only compiles the standard library of managed Python versions; the official `python` image is not precompiled.

### Cache mount

```dockerfile
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
```

`UV_LINK_MODE=copy` silences link warnings when cache and target are on different file systems. Without a cache mount use `--no-cache` or `UV_NO_CACHE` to cut image size. Managed Python is not cached by default: set `UV_PYTHON_CACHE_DIR=/root/.cache/uv/python` alongside the mount. Find the cache with `uv cache dir`, or fix it with `UV_CACHE_DIR`.

### Intermediate layers

Install dependencies first (project changes often, dependencies rarely), mounting only `uv.lock`:

```dockerfile
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

Use `--no-install-package <name>` to skip specific packages. In a workspace use `--no-install-workspace` for the first sync. The first sync uses `--frozen` because without the `pyproject.toml` files uv cannot assert the lockfile is current; the final `--locked` sync validates it.

### Non-editable multi-stage

`uv sync` and `uv run` accept `--no-editable`. Build in a builder stage with `uv sync --locked --no-editable`, set `ENV UV_PYTHON_DOWNLOADS=0` so both stages use the system Python, then in the final stage copy only the environment:

```dockerfile
COPY --from=builder /app/.venv /app/.venv
CMD ["/app/.venv/bin/hello"]
```

### Temporary uv

If the final image does not need uv: `RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv uv sync`.

### pip interface

`RUN uv pip install --system ruff`, or `ENV UV_SYSTEM_PYTHON=1`; or create a venv with `uv venv /opt/venv` and set `VIRTUAL_ENV=/opt/venv` and PATH (then omit `--system`).

## Verify

Images are signed. The page's check:

```console
$ gh attestation verify --owner astral-sh oci://ghcr.io/astral-sh/uv:latest
```

Success prints "Verification succeeded!". Prefer a version tag or digest over `latest`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/docker). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
