---
id: computing-software.devops-ci-cd.earthly.earthly-ls-doc-prune
name: earthly-ls-doc-prune
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, ls, doc, prune, earthly-ls, earthly-doc, cache-reset]
level: practitioner
status: docs-checked
description: "List Earthfile targets with earthly ls, print target doc comments with earthly doc, and clear the BuildKit cache with earthly prune --all, --reset, --age and --size."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# earthly ls, doc and prune

## earthly ls
`earthly ls [<earthfile-ref>]` prints all targets in an Earthfile in a project.
- `--args` shows `ARG` statements of the targets.
- `--long` shows full canonical target references (includes the project part if applicable).

## earthly doc
`earthly doc [<earthfile-ref>[+<target-ref>]]` prints documentation comments. A target's documentation is a comment block that ends on the line immediately above the target definition and begins with the target's name.

```
# build runs 'go build' and saves the artifact locally.
build:
    FROM +deps
    ...
```
```
$ earthly doc
TARGETS:
  +build
    build runs 'go build' and saves the artifact locally.
$ earthly doc +build
+build
  build runs 'go build' and saves the artifact locally.
```
Unlike `earthly ls`, undocumented targets (such as `deps` in the docs example) are not listed.

## earthly prune
Eliminates the Earthly cache.
```
earthly [options] prune (--all|-a)
earthly [options] prune --reset
```
- Standard form issues a prune command to the BuildKit daemon; `--all|-a` issues a "prune all".
- `--reset` restarts the BuildKit daemon and deletes the cache directory on startup, starting from scratch.
- `--age`: prune cache older than a duration string (decimal numbers with unit suffix such as `300ms`; units `ns`, `us`, `ms`, `s`, `m`, `h`).
- `--size`: prune to a specified size, oldest cache first, until the target size is reached or exceeded.

## Checked

2026-11-07. Read the ls, doc and prune sections of earthly-command.md (about lines 334-461), not the whole page. Flags and size/age units match. Nothing removed.
Method: documentation only; no commands were run.
