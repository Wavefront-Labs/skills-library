---
id: computing-software.devops-ci-cd.earthly.earthfile-locally-cache-git-clone
name: earthfile-locally-cache-git-clone
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, locally, cache, git-clone, persist, sharing, host-execution]
level: practitioner
status: docs-checked
description: "Run targets on the host with LOCALLY, add persistent CACHE mountpoints (--sharing, --id, --persist), and clone repos cache-aware with GIT CLONE in an Earthfile."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LOCALLY, CACHE and GIT CLONE

## LOCALLY
`LOCALLY` replaces `FROM` and runs the target's commands on the host rather than in a container. Nothing is cached, and results may differ between machines, so use with caution. Only `RUN`, `RUN --push`, `SAVE ARTIFACT` and `COPY` are supported. Commands see the env vars exposed to `earthly`, and the working directory is the Earthfile location.
```Dockerfile
whoami:
    LOCALLY
    RUN echo "I am currently running under $USER on $(hostname) under $(pwd)"
```
Local output of images and artifacts only happens at the end of a successful build, so inside `LOCALLY`:
- images: use `WITH DOCKER --load=+my-image`, not `BUILD +my-image` (the image would not be available).
- artifacts: use `COPY +my-artifact/my-example-artifact ./`, not `SAVE ARTIFACT ... AS LOCAL` plus `BUILD`.

## CACHE
`CACHE [--sharing <sharing-mode>] [--chmod <octal-format>] [--id <cache-id>] [--persist] <mountpoint>` creates a directory shared between instances of the same target and kept between builds.
- `--sharing`: `locked` (default; concurrent builds wait), `shared`, or `private` (a concurrent build gets a new empty cache).
- `--chmod`: octal permissions; default `0644`.
- `--id`: a global cache volume used across targets or Earthfiles.
- `--persist`: copy the cache contents into children that inherit from the target. Version 0.7 persisted by default, bloating pushed images; 0.8 changed the default so persistence needs `--persist`.

## GIT CLONE
`GIT CLONE [--branch <git-ref>] [--keep-ts] <git-url> <dest-path>` is cache-aware (distinguishes commit IDs) and uses the git auth passed to `earthly`, unlike `RUN git clone`. It is a shallow, single-depth clone. `--branch` points HEAD at the ref; default is remote HEAD. For a full clone:
```Dockerfile
GIT CLONE <git-url> <dest-path>
WORKDIR <dest-path>
ARG git_hash=$(git rev-parse HEAD)
RUN git remote set-url origin <git-url> # only required if using authentication
RUN git fetch --unshallow
```
Since v0.7.21 git credentials are not stored in `.git/config`, so fetches or pushes need `RUN git remote set-url origin <git-url>` first.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
