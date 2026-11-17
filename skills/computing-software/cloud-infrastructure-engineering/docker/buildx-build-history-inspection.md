---
id: computing-software.cloud-infrastructure-engineering.docker.buildx-build-history-inspection
name: buildx-build-history-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, buildx-history, build-history, build-records, cache-miss-debugging, opentelemetry]
level: practitioner
status: docs-checked
description: "Query past builds with docker buildx history ls/inspect/logs/export/trace to compare durations, cache hits, errors and attestations across builds and CI runs."
sources: ["https://docs.docker.com/reference/cli/docker/buildx/history/", "https://docs.docker.com/build/ci/github-actions/build-summary/", "https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# buildx build history

BuildKit keeps a record of every build (status, timings, steps, logs, provenance) in the
builder. `docker buildx history` reads those records from the CLI; Docker Desktop's Builds
view shows the same data. Commands arrived in recent buildx releases; run
`docker buildx history --help` to see what your version has.

## Commands
```bash
docker buildx history ls                         # recent builds: ref, name, status, duration
docker buildx history ls --filter status=error --format json
docker buildx history inspect                    # latest build: inputs, steps (% cached), materials, attachments
docker buildx history inspect ^1                 # the build before the latest
docker buildx history inspect <ref> --format json
docker buildx history inspect attachment <ref>   # provenance/SBOM attached to the record
docker buildx history logs <ref>                 # full plain logs after the fact
docker buildx history export <ref> -o build.dockerbuild   # import into Docker Desktop
docker buildx history trace <ref>                # OpenTelemetry trace viewer of step timing
docker buildx history rm <ref>
```
Use `--builder <name>` to read records from a non-default builder. Most subcommands accept a
build ID from `history ls` or a relative offset (`^0` or none is the latest build, `^1` the one
before, and so on); offsets work for `logs` and `inspect` among others.

## Typical tasks
**Why did this build get slow?** Inspect two refs and compare the `Build Steps` line (for
example `16/16 (25% cached)`); the first step that is no longer cached is where your cache key
changed (see the cache invalidation skill).

**What failed in CI last night?** The GitHub Actions job summary has a link to download a
build record archive (a ZIP file) that you can import into Docker Desktop's Builds view. Use
`history export` to produce a `.dockerbuild` archive from a local builder.

**What went into the image?** `history inspect` prints a `Materials` table (for example the
Dockerfile frontend and base image digests) and the attachments (provenance, SBOM) of the
record.

## Gotchas
- BuildKit keeps a limited history: the `[history]` section of `buildkitd.toml` has `maxAge`
  (seconds) and `maxEntries` (default 50 when the section is omitted); `maxEntries = 0` stops
  recording new history. Export records you need to keep.
- `history rm` removes records from the current builder; `--all` removes every record.
- Build records describe build inputs; treat exported archives as sensitive.

## Checked

Checked 2026-10-23 against the docker/buildx `docs/reference/buildx_history*.md` pages, the Docker docs GitHub Actions build-summary page and the BuildKit `docs/buildkitd.toml.md` (main branch).

- Subcommands `ls`, `inspect`, `inspect attachment`, `logs`, `export`, `trace`, `rm` (plus `import`, `open`), the `^N` offset references, `--filter status=error`, `--format json`, `--builder`.
- `history inspect` output fields (Build Steps with percent cached, Materials, Attachments).
- `[history]` `maxAge` / `maxEntries` settings in `buildkitd.toml`.
- Removed the `jq` pipe, the claim that removing a builder deletes history, and the claim that the GitHub summary artifact is a `.dockerbuild` file (the docs describe a ZIP build record archive).

Method: documentation only; no commands were run.
