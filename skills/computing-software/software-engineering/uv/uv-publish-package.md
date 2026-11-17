---
id: computing-software.software-engineering.uv.uv-publish-package
name: uv-publish-package
category: computing-software
field: software-engineering
product: uv
tags: [uv, publish, build, uv-publish, trusted-publishing, pypi, test-index, attestations]
level: practitioner
status: docs-checked
description: "Build, version and publish a package with uv build, uv version --bump and uv publish, including tokens, trusted publishing, a test index and retries."
sources: [https://docs.astral.sh/uv/guides/package/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building and publishing a package with uv

Goal: produce distributions and upload them to PyPI or another index.

## Method

1. Have a `[build-system]` in pyproject.toml (`uv init` adds one). Without it uv skips building the project on `uv sync` and falls back to legacy setuptools on `uv build`.
2. Build: `uv build` writes to `dist/`. `uv build <SRC>` builds another directory; `uv build --package <PACKAGE>` builds a workspace member. Run `uv build --no-sources` before publishing to check the package builds with `tool.uv.sources` disabled, as other build tools will.
3. Version: `uv version 1.0.0`; preview with `--dry-run`; `uv version --bump minor`. Components: major, minor, patch, stable, alpha, beta, rc, post, dev; several `--bump` flags apply largest to smallest; `--bump dev=66463664` sets a value. Examples: `--bump patch --bump beta` takes 1.3.0 to 1.3.1b1; `--bump beta` takes 1.3.0b1 to 1.3.0b2; `--bump stable` takes 1.3.1b2 to 1.3.1. This locks and syncs by default; `--frozen` prevents both, `--no-sync` prevents syncing.
4. Publish: `uv publish`. Credentials: `--token` or `UV_PUBLISH_TOKEN`; or `--username`/`UV_PUBLISH_USERNAME` with `--password`/`UV_PUBLISH_PASSWORD`. PyPI no longer takes passwords: use a token, equivalent to username `__token__`. From GitHub Actions or another Trusted Publisher no credentials are needed; add a trusted publisher on the PyPI project. uv then tries to invalidate the short-lived token afterwards (a failure only warns); explicit tokens are not revoked.
5. Test index:

```toml
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
explicit = true
```

Then `uv publish --index testpypi`. This needs pyproject.toml present (a checkout step in CI).

## Gotchas

- Partial uploads: on PyPI rerun the same command; identical files are ignored. On other registries pass `--check-url <index url>` (the index URL, not the publish URL; with `--index` it is used automatically). Existing files must match exactly.
- Attestations (PEP 740) in `dist/` as `*.publish.attestation` are found and uploaded automatically; uv does not generate them. If an index rejects them use `--no-attestations` or `UV_PUBLISH_NO_ATTESTATIONS`.

## Verify

`uv run --with <PACKAGE> --no-project -- python -c "import <PACKAGE>"`; add `--refresh-package <PACKAGE>` if a cached copy interferes.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/package). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
