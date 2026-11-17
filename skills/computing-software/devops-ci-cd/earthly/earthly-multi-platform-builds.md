---
id: computing-software.devops-ci-cd.earthly.earthly-multi-platform-builds
name: earthly-multi-platform-builds
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, multi-platform, platform, qemu, build, save-image, from, binfmt]
level: practitioner
status: docs-checked
description: "Build for several CPU architectures in Earthly with BUILD --platform and FROM --platform, set up QEMU emulation, and push merged multi-manifest images with SAVE IMAGE --push."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/multi-platform.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-platform builds in Earthly

Goal: build one target for several architectures in parallel and publish a single multi-platform image.

Only `linux` is supported as the build platform OS. By default builds run on the native architecture of the runner; `--platform` overrides it. Non-native execution uses QEMU emulation.

## Set up emulation

- Docker Desktop on Mac and Windows: QEMU is included.
- Apple Silicon: Rosetta is not enabled by default. In Docker Desktop, Settings, Features in Development, tick "Use Rosetta for x86/amd64 emulation".
- Linux (Ubuntu example, run once for the privileged command):
  ```bash
  sudo apt-get install qemu-system binfmt-support qemu-user-static
  docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
  docker stop earthly-buildkitd || true
  ```
- GitHub Actions: add to every job doing a multi-platform build:
  ```yaml
  - name: Set up QEMU
    id: qemu
    uses: docker/setup-qemu-action@v1
    with:
      image: tonistiigi/binfmt:latest
      platforms: all
  ```

## Run for several platforms

```Dockerfile
build-all-platforms:
    BUILD --platform=linux/amd64 --platform=linux/arm/v7 +build
```

`+build` then runs twice in parallel. From the CLI: `earthly --platform=linux/arm64 +build`.

## Save a multi-platform image

Use `FROM --platform=linux/arm/v7 alpine:3.18` to bind a platform. When several targets save an image with the same name for different platforms, they merge on export:

```Dockerfile
build:
    FROM alpine:3.18
    ...
    SAVE IMAGE --push org/myimage:latest
```

`earthly --push +build-all-platforms` pushes one multi-manifest image (here with `linux/amd64` and `linux/arm/v7`).

## Gotcha: local tags

The docker CLI has limited multi-manifest support locally, so exported to the local daemon the architectures appear as separate tags: `org/myimage:latest`, `org/myimage:latest_linux_amd64`, `org/myimage:latest_linux_arm_v7`. The extra tags are local only; a registry push is a single multi-manifest image.

## Checked

2026-11-07. Read docs/guides/multi-platform.md in full. Linux-only scope, QEMU and Rosetta setup, BUILD --platform, --platform on the CLI, FROM --platform and local tag behaviour match. Nothing removed.
Method: documentation only; no commands were run.
