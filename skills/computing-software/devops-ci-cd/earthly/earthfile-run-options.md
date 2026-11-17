---
id: computing-software.devops-ci-cd.earthly.earthfile-run-options
name: earthfile-run-options
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, run, push, no-cache, entrypoint, privileged, network, interactive]
level: practitioner
status: docs-checked
description: "RUN command options in an Earthfile: --push, --no-cache, --entrypoint, --privileged, --network=none, --interactive, --interactive-keep and --raw-output."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RUN options in an Earthfile

Goal: control caching, pushing, privileges and interactivity of a `RUN` step.

Forms: `RUN [options...] [--] <command>` (shell form, `/bin/sh -c`) and `RUN [[options...], "<executable>", "<arg1>", ...]` (exec form). Use `--` to mark that no more RUN options follow. A trailing `\` continues the line.

## Options
- `--push`: a push command is never cached and only runs when `earthly --push` is used, e.g. `earthly --push +deploy`. Use it for uploads or changes to external environments.
- `--no-cache`: run every time. Commands after it also skip the cache; inside `WITH DOCKER`, all commands after the `WITH DOCKER` ignore the cache. Auto-skip may still skip it.
- `--entrypoint`: prepends the image entrypoint to the command, replacing `docker run`:
```Dockerfile
FROM cytopia/golint
COPY . /data
RUN --entrypoint .
```
- `--privileged`: needs `earthly --allow-privileged` (or `-P`) as well.
- `--network=none`: isolates networking and internet access.
- `--interactive` / `--interactive-keep`: opens an interactive prompt. It must be the last command in the target (except `SAVE IMAGE`), the only interactive target in the run, and not inside `LOCALLY`. You cannot `FROM` a target that contains one. `--interactive-keep` keeps the changes you make:
```Dockerfile
build:
    FROM alpine:3.18
    RUN apk add bash
    RUN --interactive-keep bash
```
- `--raw-output` (experimental, enable with `VERSION --raw-output`): prints the line without the target-name prefix.

Related options for secrets, mounts, ssh and AWS are in the run-secrets-mounts skill.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: fixed the image name `cytopia/goling` to `cytopia/golint` (the page's own example has the typo; its docker run line says golint).

Method: documentation only; no commands were run.
