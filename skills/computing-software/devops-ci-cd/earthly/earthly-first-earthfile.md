---
id: computing-software.devops-ci-cd.earthly.earthly-first-earthfile
name: earthly-first-earthfile
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, version, targets, base-target, copy-artifact, save-image, from]
level: intro
status: docs-checked
description: "Write a first Earthfile with VERSION, a base target, build and docker targets, COPY +target/artifact, per-target FROM environments, and run it with earthly +docker."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/basics/part-1-a-simple-earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Write and run a first Earthfile

Goal: build a Go binary in one target and package it as an image in another.

```Dockerfile
VERSION 0.8
FROM golang:1.15-alpine3.13
WORKDIR /go-workdir

build:
    COPY main.go .
    RUN go build -o output/example main.go
    SAVE ARTIFACT output/example AS LOCAL local-output/go-example

docker:
    COPY +build/example .
    ENTRYPOINT ["/go-workdir/example"]
    SAVE IMAGE go-example:latest
```

## How it fits together
- The file is always named `Earthfile`. `VERSION` selects which features are enabled so the script stays compatible as Earthly updates.
- Commands before the first target form the implicit `base` target inherited by every target (here: the Go image and workdir).
- Run a target with a plus sign and its name: `earthly +build`, or `earthly +docker`.
- `SAVE ARTIFACT output/example` defaults the destination to `/`, so it is referenced as `+build/example`. With `SAVE ARTIFACT output/example /some/path/to/example` it becomes `+build/some/path/to/example`.
- `COPY +build/example .` copies an artifact from another target; it also makes `+docker` depend on `+build`.
- The build context is the directory containing the Earthfile; the build environment is the container the commands run in.

## Per-target environment
A target with its own `FROM` (for example `FROM node:12-alpine3.12` in an `npm` target) runs in that image; targets without one inherit the base.

## Running
`earthly +docker` runs both targets. Independent steps run in parallel (output is interleaved, prefixed by target name), the shared base runs once, and outputs (image, files) are written only after the whole build succeeds.

```bash
docker run --rm go-example:latest   # or podman run --rm go-example:latest
```

## Gotcha
Existing Dockerfiles port easily by copying them to an Earthfile and tweaking them slightly.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: basics/part-1-a-simple-earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
