---
id: computing-software.cloud-infrastructure-engineering.docker.onbuild-triggers-and-parser-directives
name: onbuild-triggers-and-parser-directives
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, onbuild, parser-directives, escape-directive, syntax-directive, dockerfile-syntax, check-directive]
level: advanced
description: "Use ONBUILD triggers for base images that act on the child's context, and the parser directives (syntax, escape, check) that must sit at the very top of a Dockerfile."
sources: ["https://docs.docker.com/reference/dockerfile/#onbuild", "https://docs.docker.com/reference/dockerfile/#parser-directives", "https://docs.docker.com/build/buildkit/frontend/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ONBUILD triggers and parser directives

**Goal:** build "framework" base images whose children automatically copy and build their
own source, and pin the Dockerfile frontend/escape behaviour explicitly.

## Parser directives
They must be at the top of the file, before any comment, blank line or instruction, and each
may appear once. After a comment, blank line or instruction has been processed, later
`# key=value` lines are treated as plain comments. Line continuation is not supported in them.
```dockerfile
# syntax=docker/dockerfile:1
# escape=`
# check=skip=JSONArgsRecommended;error=true
```
- `syntax=` declares the Dockerfile syntax version. Without it BuildKit uses its bundled frontend;
  `docker/dockerfile:1` makes BuildKit pull the latest stable 1.x syntax before the build, and a
  more specific tag pins it. A custom frontend image can be named here too.
- `escape=` changes the escape and line-continuation character from `\` (default). It is
  mainly useful with a backtick on Windows, where `\` is the path separator. Escaping is not
  performed in a `RUN` command, except at the end of a line.
- `check=` (since Dockerfile v1.8.0) configures build checks: `skip=<Rule>,<Rule>` or `skip=all`;
  `error=true` makes warnings fail the build; combine with a semicolon
  (`skip=JSONArgsRecommended;error=true`). Rule names are case-sensitive Pascal case. With
  `error=true`, pin the syntax version so new checks in later versions do not break the build.
Directive keys are not case-sensitive and whitespace around `=` is allowed (`#syntax=...`,
`# syntax = ...`); values are case-sensitive.

## ONBUILD
```dockerfile
FROM python:3.12-slim
ONBUILD COPY requirements.txt /app/
ONBUILD RUN pip install --no-cache-dir -r /app/requirements.txt
ONBUILD COPY . /app
```
The trigger is stored in the image metadata (the `OnBuild` key, visible with `docker inspect`)
and does not affect the current build. When the image is used in a later `FROM`, the downstream
builder runs the triggers in the order they were registered, in the context of the downstream
build, as if inserted immediately after that `FROM`. If a trigger fails, the `FROM` is aborted
and the build fails. Triggers are cleared from the final image after executing, so they are not
inherited by grandchildren.
Rules and gotchas:
- `ONBUILD ONBUILD` is not allowed, and `ONBUILD` may not trigger `FROM` or `MAINTAINER`.
- As of Dockerfile syntax 1.11, `ONBUILD` can be used with instructions that copy from other
  stages or contexts (`ONBUILD COPY --from=build ...`, `ONBUILD RUN --mount=from=config,...`).
  A stage named there must be defined in the Dockerfile where the trigger fires; a named context
  must be passed to the downstream build.
- A trigger that copies the whole context makes later steps depend on it; document the context
  layout the base image expects.
- Inspect triggers before using an unknown base with `docker inspect` on the image.
## Verify
Build the base, then a child whose Dockerfile is just `FROM base`; the build output shows the
triggered steps running right after `FROM`. `docker build --check` with a `check=` directive
shows the configured rules being skipped or escalated.

## Checked

Checked 2026-10-23 against the Dockerfile reference sections Parser directives and ONBUILD (moby/buildkit docs, main).
Confirmed: directive placement and once-only rule, case rules, `syntax`, `escape`, `check` (since v1.8.0, comma and semicolon separators), ONBUILD trigger timing, clearing after firing, the `OnBuild` metadata key, `ONBUILD ONBUILD`/FROM/MAINTAINER limits and the 1.11 copy-from support. Removed unconfirmed claims about frontend pinning for reproducibility, `1-labs`, BOM handling, discontinued `:onbuild` images and target-stage behaviour.

Method: documentation only; no commands were run.
