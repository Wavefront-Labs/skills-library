---
id: computing-software.devops-ci-cd.earthly.earthfile-from-command
name: earthfile-from-command
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, from, from-dockerfile, allow-privileged, pass-args, platform, target-ref]
level: practitioner
status: docs-checked
description: "Start an Earthfile build environment with FROM (image or target ref, --platform, --allow-privileged, --pass-args) or FROM DOCKERFILE (-f, --target, --build-arg)."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FROM and FROM DOCKERFILE in an Earthfile

Goal: pick the base of a target, either an image, another target, or an existing Dockerfile.

## FROM
Synopsis: `FROM <image-name>` or `FROM [--platform <platform>] [--allow-privileged] <target-ref> [--<build-arg-key>=<build-arg-value>...]`.

Reference forms:
- Classical: `FROM alpine:latest`
- Local target: `FROM +another-target`
- Relative: `FROM ./subdirectory+some-target` or `FROM ../otherdirectory+some-target`
- Absolute: `FROM /absolute/path+some-target`
- Remote git: `FROM github.com/example/project+remote-target`

`FROM ... AS ...` is not supported. Define a new target instead and use `FROM +build` or `COPY +build/a-file ./`.

`FROM` does not mark the referenced target's images, artifacts or push commands for output; use `BUILD` for that.

Options:
- `--platform <platform>`: platform to build on.
- `--allow-privileged`: lets a remotely referenced target use privileged capabilities (no effect on local targets). The `earthly` call also needs `--allow-privileged` (or `-P`):
```bash
earthly --allow-privileged +my-target
```
- `--pass-args`: arguments are passed automatically to targets in the same Earthfile; with this flag they also propagate to an externally referenced target.
- `--build-arg <key>=<value>` is deprecated; use `--<build-arg-key>=<build-arg-value>`.

## FROM DOCKERFILE
`FROM DOCKERFILE [options...] <context-path>` inherits from an existing Dockerfile. The context path is a host path or an artifact reference to a directory holding a `Dockerfile`. A `.dockerignore` in the context root is used unless `.earthlyignore` or `.earthignore` exist.

Options: `-f <dockerfile-path>` (host path relative to the Earthfile, or an artifact reference), `--build-arg <key>=<value>`, `--target <target-name>` (multi-stage), `--platform <platform>`, and experimental `--allow-privileged` (needs `VERSION --allow-privileged-from-dockerfile 0.8`).

Split Dockerfile and context across targets:
```Dockerfile
docker:
    FROM DOCKERFILE -f +mydockerfile/Dockerfile +mybuildcontext/mydata/*
    SAVE IMAGE testimg:latest
```
`+mybuildcontext/mydata` copies the directory and contents; `+mybuildcontext/mydata/*` copies only the contents. If both are in one target, reference it twice: `FROM DOCKERFILE -f +target/dir/Dockerfile +target/dir`.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
