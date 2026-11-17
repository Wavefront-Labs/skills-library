---
id: computing-software.software-engineering.quarkus.quarkus-native-container-build
name: quarkus-native-container-build
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, native-image, mandrel, graalvm, container-build, docker]
level: practitioner
status: docs-checked
description: "Build a Linux native executable for Quarkus without a local GraalVM using a builder container, plus remote daemons, builder image choice and native image containers."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/building-native-image.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus: native executable via container build

Use this when GraalVM/Mandrel is not installed locally or the host is not Linux. A working container runtime (Docker or podman) is required; on Docker for Windows share the project drive in Docker Desktop settings and restart it.

## Build

```bash
./mvnw package -Dnative -Dquarkus.native.container-build=true
```

The runtime is auto-detected. Force it with `-Dquarkus.native.container-runtime=docker` or `=podman`; put these in `application.properties` if you always build this way.

## What to expect

A first build typically takes 3-10 minutes and 4-8 GB of RAM on the build host. If it runs past 15 minutes without output, the container runtime is probably short of memory: raise CPU and memory and retry. The output is a Linux binary whose architecture matches the builder image (usually `x86_64`), so run it in a matching Linux container, not on the host OS.

## Builder image and base image

The builder image is based on UBI 10, so the resulting executable will not run on UBI 8 or UBI 9 base images. Switch the builder with `quarkus.native.builder-image`, for example `quay.io/quarkus/ubi9-quarkus-mandrel-builder-image:{mandrel-flavor}` (flavor tag as in the docs). For GraalVM instead of Mandrel pass `-Dquarkus.native.builder-image=graalvm`. Prefer floating tags: pinning a tag loses security updates and is unsupported.

## Remote daemon

If the build fails with `Error: Invalid Path entry getting-started-1.0.0-SNAPSHOT-runner.jar` (`NoSuchFileException`), you probably use a remote daemon. Use `-Dquarkus.native.remote-container-build=true` instead of `-Dquarkus.native.container-build=true`: the local driver mounts volumes, the remote driver copies files.

## Image in one command

```bash
./mvnw package -Dnative -Dquarkus.native.container-build=true -Dquarkus.container-image.build=true
```

Or build manually from the generated `src/main/docker/Dockerfile.native-micro` (based on `quay.io/quarkus/ubi10-quarkus-micro-image`):

```bash
docker build -f src/main/docker/Dockerfile.native-micro -t quarkus-quickstart/getting-started .
docker run -i --rm -p 8080:8080 quarkus-quickstart/getting-started
```

Verify: running `./mvnw verify -Dnative` runs the integration tests (the page's `GreetingResourceIT`) against the native executable; the page's sample shows `Tests run: 2, Failures: 0, Errors: 0, Skipped: 0`. The native test start wait defaults to 60 seconds; change with `-Dquarkus.test.wait-time=300`.

## Checked

2026-11-07. Matched against the text (with includes) of: building-native-image.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: unconfirmed wording about the integration test run; now tied to the page's `GreetingResourceIT`.

Method: documentation only; no commands were run.
