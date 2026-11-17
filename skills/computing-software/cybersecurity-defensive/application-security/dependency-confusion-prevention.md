---
id: computing-software.cybersecurity-defensive.application-security.dependency-confusion-prevention
name: dependency-confusion-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [supply-chain-security, dependency-confusion, private-registry, npm-scopes, pip-index-url, namespace-reservation, artifactory]
level: practitioner
status: draft
description: "Prevent dependency confusion: scoped/namespaced internal packages, a single proxying registry, pip extra-index-url pitfalls, reserving names publicly, and detection."
sources: ["https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610", "https://learn.microsoft.com/en-us/azure/devops/artifacts/concepts/upstream-sources", "https://docs.npmjs.com/cli/v10/using-npm/scope"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency confusion prevention

If an internal package name (e.g. `acme-auth-utils`) also exists on the public registry with a higher
version, many resolvers pick the public one: an attacker publishes that name and gets code execution in
your builds.

## Controls by ecosystem
**npm**
- Use scopes for all internal packages: `@acme/auth-utils`; map the scope to your registry in `.npmrc`:
  `@acme:registry=https://npm.internal.example/`. Own the `@acme` org on npmjs.com so nobody else can publish it.
- Commit lockfiles (`package-lock.json`) with `resolved` URLs and integrity hashes; use `npm ci`.

**Python (pip)**
- `--extra-index-url` is dangerous: pip considers all indexes and picks the highest version.
  Use a single `--index-url` pointing to a proxy registry (Artifactory, Nexus, Azure Artifacts, CodeArtifact)
  that serves internal packages and proxies PyPI, with internal names taking precedence/blocked upstream.
- Hash-pinned requirements (`pip install --require-hashes -r requirements.txt`, pip-tools `--generate-hashes`).

**Maven/Gradle**: internal groupIds you control (reverse domain), repository ordering with exclusive content
filters (`exclusiveContent { forRepository {...} filter { includeGroup "com.acme" } }`).
**NuGet**: package source mapping (`packageSourceMapping` in nuget.config) to bind `Acme.*` to the internal feed;
reserve the ID prefix on nuget.org.
**Go**: `GOPRIVATE=*.acme.example`, `GONOSUMDB`, private module proxy.

## Registry configuration
Azure Artifacts/Artifactory: upstream sources where a package name that exists internally is never pulled
from upstream ("allow externally-sourced versions" off). Block or quarantine newly published public packages
(minimum age policies) to reduce typosquat/malicious package risk.

## Name reservation
Publish placeholder packages with your internal names on public registries (empty, owned by your org), when
scopes/namespaces are not available.

## Detection
- SCA tools and registry audit logs: builds pulling internal-looking names from public registries.
- Inventory internal package names and periodically query public registries for collisions.

## Gotchas
- Leaked `package.json`/`requirements.txt` files in public repos or JS bundles reveal internal names.
- CI images with a default public registry config bypass developer settings.

## Verify
In a sandbox, publish a higher version of an internal name to a test public mirror and confirm builds
still resolve the internal version (or fail closed).
