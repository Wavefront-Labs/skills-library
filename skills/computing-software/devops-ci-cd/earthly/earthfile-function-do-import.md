---
id: computing-software.devops-ci-cd.earthly.earthfile-function-do-import
name: earthfile-function-do-import
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, function, do, import, global-import, allow-privileged, pass-args]
level: practitioner
status: docs-checked
description: "Reuse Earthfile logic with FUNCTION and DO, and alias Earthfile references with IMPORT (AS alias, global imports, --allow-privileged)."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FUNCTION, DO and IMPORT

## FUNCTION
`FUNCTION` marks the beginning of a reusable set of instructions that can be inserted into targets or other functions. Functions used to be called UDCs (User Defined Commands); the page notes Earthly 0.7 uses `COMMAND` instead of `FUNCTION`. Unlike `BUILD +target`, a function inherits the build context and build environment of its caller.

Key points:
- A function has its own `ARG` scope, separate from the caller. Anything needed from the caller must be passed explicitly: `DO +MY_FUNCTION --<build-arg-key>=<build-arg-value>`.
- Global imports and global args come from the `base` target of the Earthfile where the function is defined, which may differ from the caller's base.

## DO
`DO [--allow-privileged] <function-ref> [--<build-arg-key>=<build-arg-value>...]` expands and runs the function's commands. Options: `--allow-privileged` (same as `FROM --allow-privileged`) and `--pass-args` (same as `FROM --pass-args`).

## IMPORT
`IMPORT [--allow-privileged] <earthfile-ref> [AS <alias>]` aliases an Earthfile reference for later target, artifact or command references.
- Without `AS`, the alias is the last path element: `github.com/foo/bar/buz:v1.2.3` becomes `buz`.
- The reference can be any directory other than `.`. If it ends in `..`, `AS <alias>` is mandatory.
- An `IMPORT` in the `base` target is a global import, available to every target or command in the file regardless of base image.
- `--allow-privileged` extends the ability to request privileged capabilities to all invocations of the imported alias.

The page defers the function-reference and import syntax details to the Functions guide and the importing guide.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
