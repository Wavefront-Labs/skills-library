---
id: computing-software.devops-ci-cd.build-systems.fast-reproducible-cacheable-builds
name: fast-reproducible-cacheable-builds
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, build-automation, incremental-builds, build-cache, remote-cache, remote-execution, dependency-caching, lockfiles, reproducible-builds, hermetic-builds, monorepo, bazel, buck2, pants, nx, turborepo, gradle, gradle-build-cache, make, docker-layer-caching, buildkit, cache-mounts, source-date-epoch, build-graph, affected-targets]
level: practitioner
status: draft
description: "Make builds fast and reproducible: correct build graphs, lockfiles, layered and remote caches, Docker BuildKit caching, monorepo tools (Bazel, Nx, Turborepo) and hermeticity checks."
sources: ["https://reproducible-builds.org/docs/", "https://bazel.build/remote/caching", "https://docs.docker.com/build/cache/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build systems — fast, reproducible, cacheable builds

**Goal:** the same inputs always produce the same outputs, and nothing is rebuilt
unless one of its inputs changed — locally and in CI.

## 1. The model: a build is a graph of pure functions
Each step (target/task) should declare all its **inputs** (sources, deps, tool versions,
env vars, flags) and **outputs**. If that's true, its output can be cached by a hash of the
inputs and reused anywhere. Every caching bug is an undeclared input: a tool read from
`PATH`, the current time, an env var, a file outside the declared sources, the network.

## 2. Pin everything first (reproducibility before speed)
- Lockfiles committed and used strictly: `npm ci` (not `npm install`), `pip install
  --require-hashes -r requirements.txt` or `uv sync --locked`, `poetry install` with
  `poetry.lock`, `cargo build --locked`, `go mod download` + `go.sum`,
  Gradle dependency locking (`--write-locks`).
- Pin toolchains: `.nvmrc`/`packageManager` field + Corepack, `.python-version`,
  `rust-toolchain.toml`, Gradle wrapper, `go` directive/toolchain in `go.mod`, base images
  by digest (`FROM python:3.12-slim@sha256:...`).
- Remove time and path from outputs: set `SOURCE_DATE_EPOCH` (e.g. to the last commit
  time, `git log -1 --format=%ct`), use `-trimpath` for Go, strip build-dir paths, sort
  file lists when creating archives.
- Test it: build twice in clean environments and compare digests (`sha256sum`, or
  `diffoscope` to see *why* they differ).

## 3. Cache layers, from cheapest to most powerful
1. **Dependency cache** in CI keyed on the lockfile hash (package manager download caches).
2. **Docker BuildKit** caching:
   - order the Dockerfile so rarely-changing steps come first (copy lockfile → install →
     copy source → build);
   - cache mounts for package managers:
     `RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt`;
   - export/import layer cache in CI:
     `docker buildx build --cache-from type=registry,ref=<registry>/app:buildcache --cache-to type=registry,ref=<registry>/app:buildcache,mode=max .`
     (or `type=gha` on GitHub Actions). `mode=max` also caches intermediate stages.
   - a `.dockerignore` excluding `.git`, `node_modules`, build outputs — otherwise any
     change invalidates the `COPY . .` layer.
3. **Task-output cache:** Gradle build cache (`org.gradle.caching=true`, plus a remote
   cache node), Nx/Turborepo local + remote cache, ccache/sccache for C/C++/Rust.
4. **Remote cache + remote execution** (Bazel, Buck2, Pants): shared across all CI runs and
   developers; `bazel build --remote_cache=grpcs://<cache-host> //...`.
**Gotcha:** let developer machines *read* the remote cache but only CI *write* it, so an
unpinned laptop toolchain can't poison everyone's results.

## 4. Monorepos
- Build/test only what changed and what depends on it: `nx affected -t test --base=origin/main`,
  `turbo run test --filter=...[origin/main]`, `bazel query 'rdeps(//..., set(<changed targets>))'`.
  Run the full graph on main or nightly to catch missing edges.
- Pick the tool by ecosystem and scale: Nx/Turborepo for JS/TS-heavy repos with low setup
  cost; Bazel/Buck2/Pants for polyglot repos needing hermetic, remote-executed builds,
  at a real cost in BUILD-file maintenance and learning curve.
- Enforce boundaries (Nx module-boundary rules, Bazel `visibility`) or the graph turns into
  a hairball where everything depends on everything and nothing is cacheable.

## 5. Finding where time goes
- Gradle `--scan` or `--profile`; Bazel `--profile=prof.gz` then `bazel analyze-profile`;
  `turbo run build --summarize`; `docker buildx build --progress=plain` shows `CACHED` per step.
- Low cache hit rate → diff the input hashes of two runs of the same task to find the
  volatile input (Gradle and Bazel both offer execution-log comparisons).

## Unconfirmed
Flag spellings (Turborepo filter syntax in particular) change between major versions;
check current docs. Not hands-on verified in this sandbox.

## Verify
- [ ] Two clean builds of the same commit produce identical artifact digests (or the differences are understood).
- [ ] A no-op CI rerun is mostly cache hits (e.g. > 90% of tasks restored).
- [ ] Changing one leaf package rebuilds/tests only it and its dependents.
- [ ] Only CI has write access to the remote cache.
- [ ] Base images, toolchains and dependencies are pinned and updated by a bot, not by drift.
