---
id: computing-software.devops-ci-cd.earthly.earthfile-builtin-args
name: earthfile-builtin-args
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, builtin-args, earthly-git-hash, targetplatform, earthly-target, platform, git-args]
level: practitioner
status: docs-checked
description: "Use Earthly builtin args such as EARTHLY_TARGET_TAG, EARTHLY_GIT_HASH, EARTHLY_CI, TARGETPLATFORM and NATIVEARCH; they must be pre-declared with ARG and cannot be overridden."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/builtin-args.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Builtin args

Builtin args are filled in by Earthly and their value can never be overridden. They must be declared before use:
```Dockerfile
ARG EARTHLY_TARGET
RUN echo "The current target is $EARTHLY_TARGET"
```
To get an overridable value, derive another arg:
```Dockerfile
ARG EARTHLY_TARGET_TAG
ARG TAG=$EARTHLY_TARGET_TAG
SAVE IMAGE --push some/name:$TAG
```

## General
`EARTHLY_CI` (true when run in `--ci` mode), `EARTHLY_BUILD_SHA`, `EARTHLY_LOCALLY` (true under `LOCALLY`), `EARTHLY_PUSH` (true when `--push` was passed), `EARTHLY_VERSION` (e.g. `v0.8.0`).

## Target
For `github.com/bar/buz/src:john/work+foo`: `EARTHLY_TARGET_NAME` = `foo`; `EARTHLY_TARGET_PROJECT_NO_TAG` = `github.com/bar/buz/src`; `EARTHLY_TARGET_PROJECT` = `github.com/bar/buz/src:john`; `EARTHLY_TARGET_TAG` = `john/work` (empty if no canonical form); `EARTHLY_TARGET_TAG_DOCKER` = `john_work` (docker-safe, `latest` if no canonical form); `EARTHLY_TARGET` = the full canonical reference.

## Git
Empty string when no git directory is detected: `EARTHLY_GIT_BRANCH`, `EARTHLY_GIT_HASH`, `EARTHLY_GIT_SHORT_HASH` (first 8 chars), `EARTHLY_GIT_ORIGIN_URL`, `EARTHLY_GIT_PROJECT_NAME`, `EARTHLY_GIT_REFS` (space-separated), `EARTHLY_GIT_CO_AUTHORS`, `EARTHLY_GIT_COMMIT_TIMESTAMP`, `EARTHLY_GIT_COMMIT_AUTHOR_TIMESTAMP`, `EARTHLY_GIT_AUTHOR` (email; name too with the `--earthly-git-author-individual-args` flag, which also adds `EARTHLY_GIT_AUTHOR_EMAIL` and `EARTHLY_GIT_AUTHOR_NAME`). `EARTHLY_SOURCE_DATE_EPOCH` is the commit timestamp, or `0` with no git directory. A frequently changing hash or short hash can defeat the cache.

## Platform
`NATIVEARCH/OS/PLATFORM/VARIANT` describe the build runner; `TARGETARCH/OS/PLATFORM/VARIANT` the platform being built for (defaults to native); `USERARCH/OS/PLATFORM/VARIANT` the machine running `earthly`.

Override the target platform with `earthly --platform linux/amd64 +my-target`, `BUILD --platform linux/amd64 +my-target`, or `FROM --platform linux/amd64 alpine:3.13`. Under `LOCALLY`, `TARGETPLATFORM` is always the user platform and the flag is ignored; declare it after `LOCALLY`:
```Dockerfile
my-target:
    LOCALLY
    ARG TARGETPLATFORM
    RUN echo "The target platform under LOCALLY is $TARGETPLATFORM"
```

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/builtin-args.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
