---
id: computing-software.cloud-infrastructure-engineering.docker.circleci-setup-remote-docker-and-machine-executors
name: circleci-setup-remote-docker-and-machine-executors
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, setup-remote-docker, circleci-docker, circleci, docker-layer-caching, machine-executor, remote-docker]
level: practitioner
status: docs-checked
description: "Build Docker images on CircleCI: setup_remote_docker with the docker executor, machine executors, docker layer caching, Docker version tags, and pushing with contexts."
sources:
  - https://circleci.com/docs/building-docker-images/
  - https://circleci.com/docs/docker-layer-caching/
  - https://circleci.com/docs/configuration-reference/#machine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CircleCI setup_remote_docker and machine executors

## Docker executor + remote Docker
When the primary executor is a Docker container, Docker commands (`docker build`, `docker compose`) need the
`setup_remote_docker` key. CircleCI describes "remote" as a legacy term: the Docker commands execute on the VM that
spins up the primary container, using a machine resource class mapped from the executor's class.
```yaml
version: 2.1
jobs:
  build:
    docker:
      - image: cimg/base:current
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true      # DLC is available on all plans
      - run: |
          echo "$REGISTRY_TOKEN" | docker login ghcr.io -u "$REGISTRY_USER" --password-stdin
          docker build -t ghcr.io/org/app:${CIRCLE_SHA1} .
          docker push ghcr.io/org/app:${CIRCLE_SHA1}
workflows:
  main:
    jobs:
      - build: { context: registry-creds }
```
- CircleCI convenience images have the Docker CLI preinstalled; a third-party image needs it installed
  (for example `apk add docker-cli` on Alpine).
- Choose the engine with `setup_remote_docker: { version: <tag> }`. Documented tags: `default`, `edge` and `previous`
  (all resolve to Docker 28), `docker29`, `docker27`, `docker26`, and `20.10.24` (deprecated Docker 20).
- `prefer_same_region: true` makes a best-effort pull from the VM's region.
- Arm executors map to Arm machine resource classes for remote Docker (for example `arm.medium`); the Arm gen2
  classes are documented as beta.

## Machine executor
A VM: you do not need `setup_remote_docker` when the executor is `machine`.
```yaml
jobs:
  integration:
    machine:
      image: <MACHINE_IMAGE>        # pick from CircleCI's current machine image list
    steps:
      - checkout
      - run: docker compose up -d
      - run: ./scripts/integration-tests.sh
```
Use machine for integration tests with Compose; use the docker executor + `setup_remote_docker` for simple
build-and-push.

## Caching
- Docker Layer Caching (DLC) caches layers of images built during jobs and reuses unchanged layers on later runs; it
  is available on all CircleCI plans. With parallelism each VM has a separate DLC cache, and CircleCI uses the
  last-saved cache for the next build.
- With buildx and DLC, name your builders so CircleCI can preserve their volumes. Registering QEMU binfmt handlers
  (`tonistiigi/binfmt --install all`) can corrupt the DLC cache.
- Alternative: BuildKit registry cache (the `ref` must differ from the image you push):
```bash
docker buildx create --use
docker buildx build --cache-from type=registry,ref=ghcr.io/org/app:cache --cache-to type=registry,ref=ghcr.io/org/app:cache,mode=max -t ghcr.io/org/app:${CIRCLE_SHA1} --push .
```

## Secrets
Store registry credentials in a **context**: only organization administrators can restrict a context (security groups,
project restrictions, expression restrictions). For short-lived cloud credentials use CircleCI OIDC tokens
(`$CIRCLE_OIDC_TOKEN_V2` still works; CircleCI recommends `$CIRCLE_OIDC_TOKEN_V3` for new setups).

## Verify
- [ ] Image pushed with the commit SHA tag; rebuild shows cached layers (DLC or registry cache).
- [ ] Integration tests run on the machine executor.

## Checked
2026-10-28. Confirmed on CircleCI "Building Docker images" (remote Docker semantics, version tags and Docker versions,
prefer_same_region, Arm classes), "Docker layer caching" (all plans, parallelism, buildx naming, binfmt warning),
"Contexts" (restrictions), "OpenID Connect tokens" (V2/V3), Docker's registry cache backend page (`ref`, `mode`).
Corrected: DLC is not paid-only; remote Docker is not described as a separate host. Removed: bind-mount and port
limitation claims, `ubuntu-2204:current`, `arm.*` machine advice, `--wait` flag.
Method: documentation only; no commands were run.
