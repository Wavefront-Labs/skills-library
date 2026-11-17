---
id: computing-software.cloud-infrastructure-engineering.docker.buildkit-stage-skipping-vs-legacy-builder
name: buildkit-stage-skipping-vs-legacy-builder
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, multi-stage, stage-skipping, legacy-builder, buildkit, docker-buildkit-0, parallel-stages, build-graph]
level: practitioner
description: "How BuildKit builds only the stages your target needs and runs independent stages in parallel, versus the legacy builder's sequential all-stages behaviour, and how to detect which you are on."
sources: ["https://docs.docker.com/build/building/multi-stage/#differences-between-legacy-builder-and-buildkit", "https://docs.docker.com/build/buildkit/", "https://github.com/docker/cli/blob/master/docs/deprecated.md#legacy-builder-for-linux-images", "https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md", "https://docs.docker.com/reference/cli/docker/buildx/create/"]
status: docs-checked
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Stage skipping and parallelism: BuildKit vs the legacy builder

**Goal:** understand why the same multi-stage Dockerfile can build much faster on one machine
than another, and why a stage you expected to run (or not run) did the opposite.

## What BuildKit does
BuildKit builds only the stages that the target stage depends on (`--target X`, or the last
stage by default), following `FROM <stage>` and `COPY --from` references. Stages not on that
path are skipped. Independent stages can be built concurrently; the Docker docs describe
BuildKit as improving performance, storage management and extensibility over the legacy builder.

Example:
```dockerfile
FROM alpine AS a
RUN echo a
FROM alpine AS b
RUN echo b
FROM alpine AS c
COPY --from=a /etc/hostname /a
```
`docker build --target c .` runs `a` and `c`; `b` is skipped. `docker build .` (default =
last stage, `c`) also skips `b`. This surprises people who put a `test` stage in the middle
and assume it runs.

## What the legacy builder does
The legacy Docker Engine builder (`DOCKER_BUILDKIT=0 docker build`) processes all stages
leading up to the selected `--target`, even a stage the target does not depend on. So in the
example, `--target c` also processes `b`. The legacy builder for Linux images is deprecated
since Docker v23.0, which uses BuildKit by default (through the Buildx component) for `docker
build`; BuildKit is the default builder for Docker Desktop and Docker Engine, and Windows
containers use the legacy builder.

## Consequences to design for
- Want a stage to always run? Make the final stage depend on it (`COPY --from=stage`).
- Want to limit parallelism on a small CI runner? `buildkitd.toml` has a `max-parallelism`
  option under `[worker.oci]` (limit on parallel build steps); apply the file to a
  `docker-container` builder with `docker buildx create --buildkitd-config buildkitd.toml`.
- Parallel stages that share a `--mount=type=cache` directory should use `sharing=locked`
  (as in the Dockerfile reference's apt example) or separate `id=` values.
- Stage order in the file does not imply execution order; do not rely on side effects.

## Gotchas
- An unreferenced sibling stage is skipped under BuildKit, so a test stage can look "green"
  simply because it never ran. Check the `--progress=plain` output in CI.

## Verify
Run `docker build --progress=plain --target c .` under BuildKit and confirm no step of stage `b`
appears; with `DOCKER_BUILDKIT=0` (where still available) the legacy builder processes it.

## Checked

Checked 2026-10-23 against the Docker docs multi-stage page ("Differences between legacy builder and BuildKit"), the BuildKit overview, docker/cli `docs/deprecated.md`, the BuildKit `docs/buildkitd.toml.md` and docker/buildx `buildx create` reference.

- BuildKit builds only the stages the target depends on; the legacy builder processes all stages leading up to the target.
- Legacy builder for Linux images deprecated in v23.0 (BuildKit default through Buildx); Windows containers use the legacy builder.
- `max-parallelism` under `[worker.oci]`; the buildx flag is `--buildkitd-config` (the draft's `--config` is not in the reference).
- Removed unverified timings, the claim that legacy stages run sequentially, builder-detection heuristics and the claim about unsupported legacy flags.

Method: documentation only; no commands were run.
