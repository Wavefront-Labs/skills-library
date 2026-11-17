---
id: computing-software.devops-ci-cd.build-systems.dependency-caching-and-reproducible-builds
name: dependency-caching-and-reproducible-builds
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, reproducible-builds, deterministic-builds, bit-for-bit, dependency-proxy, pull-through-cache, artifactory, nexus, verdaccio, devpi, goproxy, athens, registry-mirror, vendoring, go-mod-vendor, cargo-vendor, offline-builds, air-gapped, lockfile-integrity, require-hashes, snapshot-debian, source-date-epoch, rewrite-timestamp, diffoscope, reprotest, trimpath, nondeterminism]
level: advanced
status: draft
description: "Make builds immune to registry outages and bit-for-bit repeatable: dependency proxies, vendoring, hash-verified lockfiles, OS package snapshots, diffoscope."
sources: ["https://reproducible-builds.org/docs/", "https://reproducible-builds.org/docs/source-date-epoch/", "https://diffoscope.org/", "https://docs.docker.com/build/ci/github-actions/reproducible-builds/", "https://go.dev/ref/mod#module-proxy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency caching and reproducible builds

**Goal:** (1) a build never fails or changes because a public registry is slow, down,
or serving a different file than yesterday; (2) building the same commit twice, on
different machines, yields byte-identical artifacts.

(Lockfile/toolchain pinning basics and task-output caching are in
`computing-software.devops-ci-cd.build-systems.fast-reproducible-cacheable-builds`; CI cache
keys are in `computing-software.devops-ci-cd.ci-pipeline-design.build-caching-strategies`.)

## 1. Put a proxy between your builds and the internet
A pull-through cache (Artifactory, Nexus, or single-ecosystem tools: Verdaccio for npm,
devpi for PyPI, Athens or any `GOPROXY` for Go, a registry mirror / pull-through cache
for container images) gives you:
- **Availability:** upstream outages and rate limits (Docker Hub pull limits) stop breaking CI.
- **Retention:** packages yanked or deleted upstream still resolve for old commits.
- **Control:** a single place to block known-bad versions and to keep internal names from
  resolving publicly.
Point every tool at it, in-repo where possible: `.npmrc` `registry=`, `pip.conf`
`index-url` (replace, don't `extra-index-url`), `GOPROXY=https://<proxy>,off`
(`off` = fail rather than bypass), Gradle/Maven repository mirrors, Docker daemon
`registry-mirrors` or fully-qualified image names through the proxy.

## 2. Verify, don't just fetch
A proxy is only as trustworthy as its integrity checks:
- npm/pnpm/yarn lockfiles carry `integrity` (SHA-512) per package — use `npm ci`.
- pip: `--require-hashes` with hashes in `requirements.txt` (`pip-compile --generate-hashes`,
  `uv pip compile --generate-hashes`).
- Go: `go.sum` + checksum database (`GOSUMDB`); keep `GOFLAGS=-mod=readonly` in CI.
- Cargo: `Cargo.lock` checksums; `--locked`.
- Gradle: dependency verification (`gradle/verification-metadata.xml`,
  `--write-verification-metadata sha256`).
- Container base images: pin `@sha256:` digests.

## 3. When to vendor
Vendoring (committing or archiving all deps) suits air-gapped builds, regulated
environments needing a full source escrow, and long-term-support branches.
- Go: `go mod vendor` (builds use it automatically with a `vendor/` dir present).
- Rust: `cargo vendor` + `.cargo/config.toml` source replacement.
- Python: `pip download -r requirements.txt -d wheelhouse/` then
  `pip install --no-index --find-links wheelhouse/`.
- JS: offline mirror (`yarn` offline cache) or `pnpm fetch` into a store.
Cost: big diffs on every update and review fatigue; most teams prefer proxy + hashes.

## 4. OS packages are the usual leak
`apt-get update && apt-get install curl` in a Dockerfile gives a different result each
week. Options: install pinned versions (`curl=8.5.0-2`), use a dated snapshot mirror
(`snapshot.debian.org/archive/debian/<timestamp>/`; Ubuntu has a similar snapshot service
*on newer releases — verify*), or build on distroless/minimal images that need no
package installs. Wolfi/Chainguard and Nix/Guix take this further (fully pinned package sets).

## 5. Make outputs deterministic
Common sources of different bytes from the same input:
| Source | Fix |
|---|---|
| Timestamps in archives/binaries | `SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)`; tools that honour it (gzip `-n`, `tar --mtime --sort=name --owner=0 --group=0 --numeric-owner`) |
| File ordering | sort inputs; `tar --sort=name`; zip tools with sorted entries |
| Absolute build paths | Go `-trimpath`; GCC/Clang `-ffile-prefix-map=$PWD=.`; Rust `--remap-path-prefix` |
| Locale, timezone, umask | set `LC_ALL=C TZ=UTC`, `umask 022` in the build |
| Embedded hostname/user/build IDs | remove or derive from commit; Go `-buildvcs` gives commit info deterministically |
| Parallel build output order | deterministic linker/archiver flags; sort generated lists |
| Container layer timestamps | BuildKit: `SOURCE_DATE_EPOCH` build arg plus `rewrite-timestamp=true` on the image exporter (BuildKit ≥ 0.13; *verify flag spelling for your version*) |

## 6. Prove it
- Build twice in clean environments (two CI runners, or `reprotest` which varies time,
  path, locale, user) and compare `sha256sum`.
- On mismatch: `diffoscope a.tar.gz b.tar.gz` recursively unpacks and shows the first
  differing field — usually a timestamp or path within minutes of looking.
- Run the comparison on a schedule; reproducibility regresses silently when someone adds
  a `date` call or a new tool.

## Verify
- [ ] CI succeeds with the public internet blocked (only the proxy reachable).
- [ ] Every ecosystem in the repo uses hash-verified installs.
- [ ] Two independent builds of the same commit produce identical digests (or the remaining diff is documented).
- [ ] Dockerfiles install OS packages pinned or from a snapshot, not from a moving mirror.
- [ ] A scheduled job re-checks reproducibility and alerts on drift.
