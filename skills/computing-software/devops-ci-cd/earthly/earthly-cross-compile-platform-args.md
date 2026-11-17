---
id: computing-software.devops-ci-cd.earthly.earthly-cross-compile-platform-args
name: earthly-cross-compile-platform-args
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, cross-compile, targetplatform, targetarch, userplatform, platform, with-docker, copy]
level: advanced
status: docs-checked
description: "Make Earthly multi-platform images without QEMU by cross-compiling, use TARGETPLATFORM and USERPLATFORM builtin args, and avoid the WITH DOCKER non-native platform limit."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/multi-platform.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cross-compiling and platform args in Earthly

Goal: produce images for other architectures without running `RUN` on them, which avoids QEMU (and is faster). Works for languages that cross-compile, such as Go and Rust.

## Cross-compile pattern

`+build` runs on the host platform, while `COPY --platform=...` with arg overrides yields a binary for the target architecture:

```Dockerfile
build:
    FROM golang:1.15-alpine3.13
    WORKDIR /example
    ARG GOOS=linux
    ARG GOARCH=amd64
    ARG GOARM
    COPY main.go ./
    RUN go build -o main main.go
    SAVE ARTIFACT ./main

build-arm-v7:
    FROM --platform=linux/arm/v7 alpine:3.18
    COPY \
        --platform=linux/amd64 \
        (+build/main --GOARCH=arm --GOARM=v7) ./example/main
    ENTRYPOINT ["/example/main"]
    SAVE IMAGE --push org/myimage:latest
```

Since `+build-arm-v7` has no `RUN`, no emulation is needed.

## Builtin platform args

`TARGETPLATFORM` (e.g. `linux/arm/v7`), `TARGETOS` (`linux`), `TARGETARCH` (`arm`), `TARGETVARIANT` (`v7`). They simplify the above:

```Dockerfile
build-all-platforms:
    BUILD --platform=linux/amd64 --platform=linux/arm/v7 +build-image

build-image:
    ARG TARGETPLATFORM
    ARG TARGETARCH
    ARG TARGETVARIANT
    FROM --platform=$TARGETPLATFORM alpine:3.18
    COPY \
        --platform=linux/amd64 \
        (+build/main --GOARCH=$TARGETARCH --VARIANT=$TARGETVARIANT) ./example/main
    ENTRYPOINT ["/example/main"]
    SAVE IMAGE --push org/myimage:latest
```

The matching `+build` there declares `ARG VARIANT` and runs `GOARM=${VARIANT#"v"} go build -o main main.go`.

## USER args

`USERPLATFORM`, `USEROS`, `USERARCH`, `USERVARIANT` describe the host that called `earthly` (`USERVARIANT` is an empty string for non-arm), useful to tell if emulation is in use.

## WITH DOCKER limit

The target containing `WITH DOCKER` must run on the native architecture of the runner; the images it runs can be any architecture. So `FROM --platform=linux/arm64 earthly/dind` does not work on amd64, but `FROM earthly/dind` with `docker run --platform=linux/arm64 earthly/examples:multiplatform` inside does. Reason given: docker-in-docker is not yet supported in a QEMU environment.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: guides/multi-platform.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
