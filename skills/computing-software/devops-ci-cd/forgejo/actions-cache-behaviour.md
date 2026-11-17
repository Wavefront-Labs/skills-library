---
id: computing-software.devops-ci-cd.forgejo.actions-cache-behaviour
name: actions-cache-behaviour
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [actions-cache, cache-proxy, zstd, podman-pasta]
level: practitioner
status: docs-checked
description: "Reuse downloads and build results with actions/cache and fix the Podman 5 Pasta networking failure."
sources:
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The cache reuses files from earlier runs, such as package downloads or intermediate build results. Some actions use it automatically, for example `setup-go` caches packages from `go.mod`. Use `actions/cache` to control what is cached and when.

Caveats:

- No guarantee that a cache is populated, even for jobs run in sequence; use artifacts for reliable hand-over.
- `actions/cache` compresses with zstd when present. A container without zstd cannot decompress such a cache and continues without it, so use zstd everywhere or nowhere.
- If the runner is not configured to provide a cache, the action fails with the error `Cache action is only supported on GHES version >= 3.5`.

Podman 5 with Pasta networking (the default) copies the host's primary IP into containers, so containers cannot reach the host through that address, which is how the cache is contacted. Either change Podman's networking, or set in the runner configuration:

```
cache:
  proxy_port: 4000
  actions_cache_url_override: 'http://host.containers.internal:4000'
```

That override suits a runner that only uses Podman, because every backend, such as LXC, would receive the same URL.

## Checked

2026-11-04. Confirmed against the Forgejo Actions advanced features page (Cache and Caching with Podman sections): the zstd caveat, the GHES error text, the Podman 5 Pasta explanation and the runner cache settings. Nothing removed.

Method: documentation only; no commands were run.
