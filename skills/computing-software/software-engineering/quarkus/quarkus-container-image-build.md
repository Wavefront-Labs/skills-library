---
id: computing-software.software-engineering.quarkus.quarkus-container-image-build
name: quarkus-container-image-build
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, container-image, jib, docker, podman, buildpack]
level: intro
status: docs-checked
description: "Build and push container images from a Quarkus build using the container-image extensions (Jib, Docker, Podman, OpenShift, Buildpack) and pick one builder."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/container-image.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus: build and push a container image

Quarkus builds images through one extension per builder. Add exactly one:

- `quarkus-container-image-jib`: no Docker client or daemon needed just to push to a registry; dependencies (under `target/lib`) sit in a separate layer so rebuilds and pushes are small.
- `quarkus-container-image-docker`: uses the Docker binary and the generated Dockerfiles under `src/main/docker`.
- `quarkus-container-image-podman`: same idea with Podman.
- `quarkus-container-image-openshift`: binary builds inside the OpenShift cluster (the Quarkus Kubernetes extension creates the `BuildConfig` and two `ImageStream` resources).
- `quarkus-container-image-buildpack`: buildpacks; needs a Docker daemon and no default builder image is provided.

## Build and push

Building is off by default. Set the property on the command line (any Quarkus config source works):

```bash
./mvnw package -Dquarkus.container-image.build=true
./mvnw package -Dquarkus.container-image.push=true
```

If no registry is set with `quarkus.container-image.registry`, `docker.io` is used. Gradle users run the integration tests on the image with `./gradlew quarkusIntTest -Dquarkus.container-image.build=true` (Maven: `./mvnw verify -Dquarkus.container-image.build=true`).

For a native image already built, add `-Dquarkus.native.reuse-existing=true` so the native build is not re-run.

## Gotchas stated by the docs

- Several container-image extensions in one build raise an error. Remove the extras or choose with `quarkus.container-image.builder=docker` (for example `docker` when both the docker and podman extensions are present).
- Jib with `build=true` and `push` unset (default `false`) still registers the image with the Docker daemon, so Docker must exist and the image shows in `docker images`.
- Docker multi-platform builds use `docker buildx build` (`quarkus.docker.buildx.platform`). More than one platform cannot be loaded locally, so you must also set `quarkus.container-image.push=true`.
- Podman builds multi-platform natively; the Docker extension also works with Podman through its Docker-compatible API.
- Buildpack: set `quarkus.buildpack.jvm-builder-image` (or `quarkus.buildpack.native-builder-image` for native), and pass `quarkus.container-image.build=true` on the command line rather than in properties to avoid nested builds.
- In GitLab CI use `quarkus.container-image.image=${CI_REGISTRY_IMAGE}`.

## Checked

2026-11-07. Read in full: container-image.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
