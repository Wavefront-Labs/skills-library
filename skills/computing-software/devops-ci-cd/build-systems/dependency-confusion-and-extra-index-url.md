---
id: computing-software.devops-ci-cd.build-systems.dependency-confusion-and-extra-index-url
name: dependency-confusion-and-extra-index-url
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, dependency-confusion, extra-index-url, dependency-proxy]
level: advanced
status: docs-checked
description: "Prevent dependency confusion with private package names: why pip --extra-index-url is unsafe, single-index proxies, npm scopes, and registry configuration per ecosystem."
sources: ["https://pip.pypa.io/en/stable/cli/pip_install/", "https://pip.pypa.io/en/stable/topics/secure-installs/", "https://docs.astral.sh/uv/concepts/indexes/", "https://docs.gradle.org/current/userguide/filtering_repository_content.html", "https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file", "https://go.dev/ref/mod"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# extra-index-url and dependency confusion

Dependency confusion (Alex Birsan, 2021): an attacker publishes a package on the public registry with the
same name as your internal package and a higher version. Resolvers that consult multiple indexes
pick the higher version.

## pip
pip checks every location given by `--index-url`, `--extra-index-url` and `--find-links` with no priority between them and picks the best match by version. Its documentation states that using `--extra-index-url` for private packages is unsafe.
Safer options:
- One index only: a proxy (Artifactory, Nexus, devpi, CodeArtifact) that serves internal packages and
  proxies PyPI, with internal names **blocked** from upstream:
  ```ini
  # pip.conf
  [global]
  index-url = https://pypi.internal.example.com/simple
  ```
- uv: its default `index-strategy` is `first-index` (it stops at the first index that has the package, to prevent dependency confusion); `unsafe-best-match` is the pip-like behaviour. Pin a package to one index with `[tool.uv.sources] mypkg = { index = "internal" }` and mark the index `explicit = true` so only pinned packages use it.
- Hash-checking mode (`--require-hashes`) stops silent swaps of a pinned package.

## npm
- Use **scopes** for internal packages (`@acme/utils`) and map the scope:
  `.npmrc`: `@acme:registry=https://npm.internal.example.com/` (npm determines the registry from the package's scope)

## Others
- Gradle: declare repositories with exclusive content (`exclusiveContent`) so internal groups resolve only from the internal repository.
- Maven: a `<mirrorOf>*</mirrorOf>` mirror to a repository manager makes every request go through one controlled endpoint.
- NuGet: package source mapping (the `packageSourceMapping` section of `nuget.config`) maps package id patterns to sources.
- Go: `GOPRIVATE` marks module path prefixes as private (no public proxy or checksum database lookup).

## Verify
- [ ] Publishing a higher-versioned same-name package to a test public registry does not change the resolved package (lockfile diff empty).

## Checked
Date: 2026-10-25. Documentation: pip `docs/html/cli/pip_install.rst` and `topics/secure-installs.md` (pypa/pip); uv `docs/concepts/indexes.md` (astral-sh/uv); Gradle user guide "Filtering Repository Content" (gradle/gradle); NuGet `nuget-config-file.md`; Go `ref/mod.md`.
Confirmed: pip has no index priority and calls `--extra-index-url` unsafe for private packages; hash-checking mode flag `--require-hashes`; uv `first-index` default, `unsafe-best-match`, `explicit = true`, `[tool.uv.sources]` index pinning; Gradle exclusive repository content; NuGet `packageSourceMapping`; `GOPRIVATE`.
Confirmed also: npm scope-to-registry mapping (npm registry and scope pages, npm/cli).
Removed: `GONOSUMDB` and the advice to register the scope name on npmjs.com (not in the pages read), and the Medium article source (replaced by documentation URLs).
Method: documentation only; no commands were run.
