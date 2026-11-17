---
id: computing-software.devops-ci-cd.earthly.earthfile-save-artifact-image-build
name: earthfile-save-artifact-image-build
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, save-artifact, save-image, build, as-local, no-manifest-list, auto-skip]
level: practitioner
status: docs-checked
description: "Export outputs from an Earthfile with SAVE ARTIFACT (AS LOCAL), SAVE IMAGE (--push) and BUILD, including which targets contribute outputs and pushes."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SAVE ARTIFACT, SAVE IMAGE and BUILD

## SAVE ARTIFACT
`SAVE ARTIFACT [--keep-ts] [--keep-own] [--if-exists] [--force] <src> [<artifact-dest-path>] [AS LOCAL <local-path>]` copies files into the target's artifact environment (dest defaults to `/`). `AS LOCAL` also writes to the host after a successful build. Inspect an artifact environment with:
```bash
earthly --artifact +<target>/* ./output/
```
Directory vs file artifacts: a directory artifact **replaces** the local destination; files are copied **into** it.
```Dockerfile
SAVE ARTIFACT ./my-directory AS LOCAL ./destination     # wipes and replaces ./destination
SAVE ARTIFACT ./my-directory/* AS LOCAL ./destination   # merges into ./destination
```
Options: `--keep-ts`, `--keep-own`, `--if-exists` (skip when missing), `--symlink-no-follow` (also needed on the matching COPY), `--force` (allow writing outside the directory containing the Earthfile).

## SAVE IMAGE
`SAVE IMAGE [--push] <image-name>...` names the target's image. Several names are allowed on one line or several lines. `--push` marks it for pushing, only done when `earthly --push` is used (e.g. `earthly --push +docker-image`); with inline caching it also makes those names cache sources. `--no-manifest-list` skips the manifest list, useful for platforms without multi-platform images such as AWS Lambda.

## BUILD
`BUILD [options...] <target-ref> [--<build-arg-name>=<build-arg-value>...]` invokes another target; sibling BUILDs without dependencies run in parallel. Arg values may be constants, expressions like `"$A and $B"` or dynamic `$(...)`. Options: `--platform` (repeatable: `BUILD --platform=linux/amd64 --platform=linux/arm/v7 +build`), `--auto-skip` (beta), `--allow-privileged`, `--pass-args`.

From VERSION 0.6, local artifacts and images are only saved, and pushes only run, for targets reached from the invoked target through a chain of `BUILD` commands. `FROM`, `COPY`, `WITH DOCKER --load` do not contribute. If you COPY from a target and want its outputs, add a `BUILD` with the same platform and args:
```Dockerfile
my-target:
    BUILD --platform=linux/amd64 +some-target --FOO=bar
    COPY --platform=linux/amd64 (+some-target/some-file.txt --FOO=bar) ./
```
Glob form `BUILD ./services/*+compile` needs `VERSION --wildcard-builds 0.8` (experimental).

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
