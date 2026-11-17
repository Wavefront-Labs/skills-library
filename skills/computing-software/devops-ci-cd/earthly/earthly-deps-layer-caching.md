---
id: computing-software.devops-ci-cd.earthly.earthly-deps-layer-caching
name: earthly-deps-layer-caching
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, layer-caching, deps-target, from-deps, copy, go-mod-download, cache]
level: practitioner
status: docs-checked
description: "Order COPY and RUN so Earthly layer caching survives code changes, and split dependency downloads into a reusable +deps target inherited with FROM +deps."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/basics/part-3-adding-dependencies-with-caching.md
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching-in-earthfiles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Layer caching: dependencies first

Goal: avoid re-downloading dependencies whenever source code changes.

## Principle
Each command's layer is reused if its inputs (ARG values, COPY'd files, the command text) are unchanged. A changed layer and everything after it re-runs, as with Dockerfile layer caching. Copy the smallest set of files before the expensive step.

```Dockerfile
# Avoid
COPY . .
RUN go mod download
RUN go build ...

# Best
COPY go.mod go.sum ./
RUN go mod download
COPY ./*.go ./
RUN go build ...
```
The first form re-runs `go mod download` after unrelated edits such as README.md or `git fetch`. The middle option (`COPY go.mod go.sum ./*.go ./`) is better but still re-downloads on every .go change.

## Reusable +deps target
```Dockerfile
deps:
    COPY go.mod go.sum ./
    RUN go mod download
    # Output these back in case go mod download changes them.
    SAVE ARTIFACT go.mod AS LOCAL go.mod
    SAVE ARTIFACT go.sum AS LOCAL go.sum

build:
    FROM +deps
    COPY main.go .
    RUN go build -o output/example main.go
    SAVE ARTIFACT output/example AS LOCAL local-output/go-example
```
`FROM +deps` inherits the dependency layer, so several targets can share it. Cross-target references create a build graph: if `target1` rebuilds an artifact that `target2` copies, part of `target2` re-runs too.

## Gotcha
Earthly treats files in a `COPY` as build inputs, so be specific; in some cases files must be listed individually.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: basics/part-3-adding-dependencies-with-caching.md, caching/caching-in-earthfiles.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
