---
id: computing-software.software-engineering.zig.container-ci
name: container-ci
category: computing-software
field: software-engineering
product: zig
tags: [zig, container-ci, zig-deployment, docker-scratch, github-actions, ci-pipeline, release-artifacts, distroless]
level: practitioner
status: docs-checked
description: "Fetch a pinned Zig toolchain in CI or a container, cross-compile with zig build -Dtarget, prefetch dependencies and cache."
sources:
  - https://ziglang.org/download/
  - https://ziglang.org/learn/build-system/
  - https://github.com/mlugg/setup-zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containers, CI pipelines and distribution
**Goal:** repeatable build and ship.

- Toolchain download URLs follow the layout shown on the download page: `https://ziglang.org/download/<version>/zig-<arch>-<os>-<version>.tar.xz` (zip for Windows), each with a `.minisig` signature; verify it with minisign using the key on that page. `https://ziglang.org/download/index.json` is the JSON version of the page and includes older releases; use it for exact tarball names rather than guessing.
- In a container build, download and unpack that tarball at a pinned `<version>`, put its directory on `PATH`, then run `zig build`.
- Build options: `-Dtarget=<triple>` and `-Doptimize=<mode>` are the standard options a `build.zig` can expose; the build-system guide shows one `zig build` producing `hello` for aarch64-macos, aarch64-linux, x86_64-linux-gnu, x86_64-linux-musl and x86_64-windows under `zig-out/<target>/`, and `zig build --summary all` prints per-step results.
- Dependencies: `zig build --fetch` fetches the dependency tree and exits (`--fetch=all` also fetches lazy dependencies; default `needed`). Run it where network is available if later build steps are offline.
- GitHub Actions: `mlugg/setup-zig@v2` installs Zig and preserves the Zig cache across runs (global cache `~/.cache/zig` on Linux; local caches are redirected into it). Pin `version:` and include matrix variables in `cache-key`.
- Build output lives in `zig-out`; the local cache directory is `.zig-cache`.
- Publishing release artifacts (checksums, signing) is not covered by the cited pages; follow your hosting platform's documentation.

## Self-check
Build the image or CI job from a clean checkout and confirm the binary appears under `zig-out`.

## Checked

2026-11-08. Read: setup-zig README in full; ziglang.org download page (release layout, minisign, index.json link) and the build-system guide (`--fetch`, target/optimize options, multi-target example) by search and targeted reads.
Removed: Dockerfile example (alpine/scratch/CA-certificate advice), distroless and sha256sum publishing advice, `zig fmt --check` CI step, claim that one Linux runner suffices for all OS tests, zig.guide source (not read).
Method: documentation only; no commands were run.
