---
id: computing-software.software-engineering.uv.uv-index-authentication
name: uv-index-authentication
category: computing-software
field: software-engineering
product: uv
tags: [uv, package-indexes, authentication, credentials, cache-control, ignore-error-codes, hash-algorithm, index]
level: practitioner
status: docs-checked
description: "Configure credentials, authenticate modes, ignored HTTP error codes, cache-control headers and hash algorithm for a private uv index."
sources: [https://docs.astral.sh/uv/concepts/indexes/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv private index authentication and per-index settings

Goal: make a private index work safely and cache sensibly.

## Method

Credentials via environment variables. For an index named `internal-proxy` defined without credentials, the variables use the uppercased name with non-alphanumerics replaced by underscores:

```sh
export UV_INDEX_INTERNAL_PROXY_USERNAME=public
export UV_INDEX_INTERNAL_PROXY_PASSWORD=koala
```

Or embed them in the URL: `url = "https://public:koala@pypi-proxy.corp.dev/simple"`. Credentials are never written to `uv.lock`, so uv needs the authenticated URL at install time.

Providers: uv can also discover credentials from netrc and keyring. It first tries an unauthenticated request, then searches for credentials if that fails; if a username is set, it searches first. Some indexes (GitLab) forward unauthenticated requests to a public index, so uv never searches; set `authenticate = "always"` per index to eagerly search and error if none is found. `authenticate = "never"` never searches and errors if credentials are given directly.

Ignored error codes: with `first-index`, uv stops searching on HTTP 401 or 403 (except 403 on the `pytorch` index). By default, an HTTP error fetching metadata or an archive stops resolution; ignoring it marks that version unavailable. Per index:

```toml
[[tool.uv.index]]
name = "private-index"
url = "https://private-index.com/simple"
authenticate = "always"
ignore-error-codes = [403]
```

A 404 always continues the search and cannot be overridden.

Cache-control: uv follows the index's headers (PyPI: metadata `max-age=600`, files `max-age=365000000, immutable`). Override for indexes that disable caching:

```toml
cache-control = { api = "max-age=600", files = "max-age=365000000, immutable" }
```

`api` covers Simple API requests, `files` covers wheels and source distributions; `api = "no-cache"` forces revalidation. The page recommends PyPI-style values.

Hash algorithm (preview): set `preview-features = ["index-hash-algorithm"]` under `[tool.uv]` and `hash-algorithm = "sha256"` on the index. If a locked distribution lacks that algorithm, uv fails rather than falling back.

Per-index `exclude-newer` is covered by uv-reproducible-resolution.

## Gotchas

- Dedicated guides exist for Azure Artifacts, Google Artifact Registry, AWS CodeArtifact and JFrog Artifactory.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/indexes). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
