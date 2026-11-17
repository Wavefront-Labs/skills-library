---
id: computing-software.devops-ci-cd.verdaccio.ci-caching-and-memory-storage
name: ci-caching-and-memory-storage
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [caching, ci-cache, maxage, tarball-cache, ci-builds, memory-plugin, cache-false]
level: practitioner
status: docs-checked
description: "Speed up CI installs with Verdaccio as a cache, save disk with uplink cache false, extend maxage, or use verdaccio-memory and verdaccio-auth-memory."
sources:
  - https://verdaccio.org/docs/caching/
  - https://verdaccio.org/docs/uplinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Verdaccio caches metadata and tarballs into storage on demand. Use cases: CI servers that clear caches per build, slow or filtered networks, offline mode shared across npm/yarn/pnpm, and protection against upstream tarballs vanishing (the left-pad issue).

Options:
```yaml
uplinks:
  npmjs:
    url: https://registry.npmjs.org/
    cache: false     # keep only metadata, no tarballs
    maxage: 30m      # default 2m before revalidating metadata
```
Higher `maxage` means fewer remote calls; good when dependencies change rarely.

Memory only (data is lost on restart):
```
npm install -g verdaccio-auth-memory verdaccio-memory
```
```yaml
auth:
  auth-memory:
    users:
      foo:
        name: test
        password: test
store:
  memory:
    limit: 1000
```
Verify: install twice with the network blocked on the second run; cached packages and versions requested before still resolve.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Caching strategies and Uplinks. Confirmed: the CI, latency, offline and left-pad scenarios, uplink cache: false, maxage with the 2m default, verdaccio-memory and verdaccio-auth-memory with the config shown. Removed or corrected: the claim that the GitHub Actions publish action uses these plugins in its image.

Method: documentation only; no commands were run.
