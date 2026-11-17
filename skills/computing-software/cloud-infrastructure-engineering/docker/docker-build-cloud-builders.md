---
id: computing-software.cloud-infrastructure-engineering.docker.docker-build-cloud-builders
name: docker-build-cloud-builders
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-build-cloud, build-cloud, cloud-builder, buildx-cloud-driver, remote-build-cache, shared-cache]
level: practitioner
status: docs-checked
description: "Use Docker Build Cloud: create cloud builders, the buildx cloud driver locally and in CI, shared team cache, native multi-platform builds, and when it beats self-hosted BuildKit."
sources:
  - https://docs.docker.com/build-cloud/
  - https://docs.docker.com/build-cloud/ci/
  - https://docs.docker.com/build/builders/drivers/cloud/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker Build Cloud builders

Docker Build Cloud runs builders hosted by Docker, each isolated to a single organisation, with a remote build cache shared by team members and native multi-platform builds (`linux/amd64` and `linux/arm64`).

## Setup
1. In the Docker Build Cloud Dashboard, create a cloud builder for your organisation (for example `acme/default`). Access comes with a paid Docker subscription, or a 7-day trial for free Personal accounts, per the Build Cloud overview.
2. Locally:
```bash
docker login
docker buildx create --driver cloud acme/default        # registers local endpoint "cloud-acme-default"
docker buildx use cloud-acme-default --global           # or pass --builder per build
docker buildx build --platform linux/amd64,linux/arm64 -t acme/api:dev --push .
docker buildx ls
```
`docker buildx use` changes the default only for `docker buildx build`; `docker build` still uses the
`default` builder unless you pass `--builder` or set `BUILDX_BUILDER`. The Docker Desktop Builds view
works with Build Cloud, including builds started by team members on the same builder.

## CI (GitHub Actions)
```yaml
- uses: docker/login-action@<version>
  with: { username: ${{ vars.DOCKER_ACCOUNT }}, password: ${{ secrets.DOCKER_ACCESS_TOKEN }} }
- uses: docker/setup-buildx-action@<version>
  with:
    driver: cloud
    endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}"   # for example "acme/default"
- uses: docker/build-push-action@<version>
  with:
    tags: acme/api:${{ github.sha }}
    outputs: ${{ github.event_name == 'pull_request' && 'type=cacheonly' || 'type=registry' }}
```
Pin each action to a current release. The `<version>` placeholders are deliberate.
- Authenticate with an organisation access token (OAT, needs the **cloud-connect** scope) if you can
  create one, otherwise a personal access token (PAT); Build Cloud only needs read access, but pushing
  to Docker Hub needs write access.
- For pull requests the example exports results to the build cache (`type=cacheonly`); otherwise it
  pushes to a registry. The docs recommend pushing directly rather than loading and then pushing.
- Builds have a timeout limit that depends on your subscription plan; longer builds are cancelled.

## Behaviour to know
- With no output specified, Buildx leaves an untagged result in the cloud build cache and does not
  load it into Docker Engine. With `--tag`, it loads the image automatically for single-platform builds on
  one cloud node; use `--load` to request loading explicitly.
- Secrets passed with `--secret` are sent encrypted and are never stored in the build cache; build
  arguments are stored in the cache and exposed through attestations, so do not pass secrets that way.
- The build cache is shared by team members using the builder, and pruning a cloud builder's cache also
  removes the cache for other team members; old cache is removed automatically when you hit your
  storage limit.
- Docker Build Cloud is only available in the US East region, per the overview page.

## When it's worth it
| Situation | Build Cloud | Self-hosted BuildKit / registry cache |
|---|---|---|
| Multi-arch builds | native `linux/amd64` and `linux/arm64` support | emulation or your own ARM runners |
| Ephemeral CI runners losing cache | persistent shared cache | registry cache (export/import cost) |
| Region requirements | US East only | wherever you host it |

## Verify
- [ ] `docker buildx ls` shows the cloud builder; a second build of an unchanged Dockerfile is mostly `CACHED`.
- [ ] A multi-platform build (`--platform linux/amd64,linux/arm64`) completes on the cloud builder.

## Checked

Date: 2026-10-24. Documentation release: Docker Build Cloud overview, setup, usage and CI pages (docker/docs main).
Confirmed: `docker buildx create --driver cloud <ORG>/<BUILDER_NAME>` and the `cloud-ORG-BUILDER_NAME` endpoint name,
`docker buildx use ... --global` scope, `BUILDX_BUILDER`, native amd64 and arm64 support, the load behaviour with and without
`--tag`/`--load`, `cacheonly` for pull requests in the CI example and its `driver: cloud`/`endpoint` inputs, token types
and the cloud-connect scope, plan-dependent timeout, secrets not stored in cache, build arguments stored in cache,
cache pruning affecting team members, US East only, and access by paid subscription or trial. Removed: action version
pins, `install: true`, the `.dockerignore` and cache-poisoning remarks, and the cost and data-residency table rows,
which the documentation does not state.

Method: documentation only; no commands were run.
