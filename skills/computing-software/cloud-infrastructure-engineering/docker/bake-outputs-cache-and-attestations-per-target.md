---
id: computing-software.cloud-infrastructure-engineering.docker.bake-outputs-cache-and-attestations-per-target
name: bake-outputs-cache-and-attestations-per-target
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, bake, bake-output, bake-cache, cache-to, cache-from, attestations, buildx-bake]
level: advanced
status: docs-checked
description: "Configure output, tags, cache-from/cache-to and attest per Bake target, parameterise cache refs by branch with variables, and override them from the CLI with --set."
sources: ["https://docs.docker.com/build/bake/reference/", "https://docs.docker.com/reference/cli/docker/buildx/bake/", "https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/metadata/attestations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bake outputs, cache and attestations per target

## Target attributes
```hcl
variable "REGISTRY" { default = "reg.example.com/team" }
variable "BRANCH"   { default = "main" }        # export BRANCH=feature-x to override

function "cache_ref" {
  params = [name, branch]
  result = "${REGISTRY}/cache:${name}-${replace(branch, "/", "-")}"
}

target "_common" {
  attest = ["type=provenance,mode=max", "type=sbom"]
}

target "api" {
  inherits   = ["_common"]
  tags       = ["${REGISTRY}/api:${BRANCH}"]
  cache-from = [
    "type=registry,ref=${cache_ref("api", BRANCH)}",
    "type=registry,ref=${cache_ref("api", "main")}",     # fallback to main's cache
  ]
  cache-to   = ["type=registry,ref=${cache_ref("api", BRANCH)},mode=max,image-manifest=true"]
  output     = ["type=image,push=true"]
}

target "binaries" {
  target = "export"
  output = ["type=local,dest=./dist"]
  cache-from = ["type=registry,ref=${cache_ref("api", BRANCH)}"]   # reuse api's build stages
}
```
Recent Bake versions also accept object syntax (`output = [{ type = "local", dest = "dist" }]`);
string syntax works everywhere.

## CLI overrides
```bash
docker buildx bake --print api                      # resolved JSON: check outputs and cache refs
docker buildx bake --push                           # = *.output=type=registry for all targets
docker buildx bake --load api                       # load into local docker
docker buildx bake --set '*.cache-to='              # empty non-append value clears the list (e.g. on PRs)
docker buildx bake --set api.output=type=docker,name=api:dev
BRANCH=$(git rev-parse --abbrev-ref HEAD) docker buildx bake
```

## Gotchas
- `--push` and `--load` are conditional: with `local` or `tar` outputs they do nothing, with
  `image` outputs `--push` sets `push=true`, and with no output defined they add an export.
  Keep exporter choice in one place.
- `max` mode caches every layer including intermediate steps; `min` (the default) caches only
  layers of the exported image. Writing to a cache location overwrites what was there, so use a
  different ref per scope (for example per branch).
- `--set` keys are singular (`tag`, `arg.NAME`, `platform`); the plural Bake names are accepted
  as aliases. `attest` already appends by default when set from the CLI.
- Attestations attach to an image index. With the `docker` driver and the classic image store
  the build fails ("Attestation is not supported for the docker driver"); use the containerd
  image store or a `docker-container` builder, and push rather than `--load` on the classic
  store.

## Checked

Checked 2026-10-23 against docker/buildx `docs/bake-reference.md` and `docs/reference/buildx_bake.md`, and the Docker docs registry cache and attestations pages (main branch).

- `attest`, `cache-from`, `cache-to`, `output` attributes (string and object syntax), `--set` override rules (empty value clears, `+=` appends, singular keys with plural aliases).
- `--push` / `--load` conditional behaviour; `--push` is `*.output=type=registry`.
- Cache `mode` default `min`; attestation requirement for an image index and the docker-driver/classic-store error.
- Removed the `type=local` plus `--push` error claim (the docs say local outputs are left alone), the storage-doubling claim, and the `--set '*.attest=...mode=min'` example (attest appends).

Method: documentation only; no commands were run.
