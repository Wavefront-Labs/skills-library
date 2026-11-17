---
id: computing-software.devops-ci-cd.earthly.earthly-build-args-and-let
name: earthly-build-args-and-let
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, arg, let, set, earthly-build-args, arg-file, build-args, variables]
level: intro
status: docs-checked
description: "Declare and override Earthly build args with ARG, command line, EARTHLY_BUILD_ARGS or an .arg file, and use LET and SET for private variables inside a target."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/build-args.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly build args, defaults and LET variables

Goal: make an Earthfile target configurable with `ARG`, supply values several ways, and keep private state with `LET`/`SET`.

## Declare and use

```Dockerfile
VERSION 0.8
FROM alpine:latest

hello:
    ARG name
    RUN echo "hello $name"
```

```bash
earthly +hello --name=world
```

An arg with no default is the empty string. Defaults may be constant or dynamic (a shell expression in `$(...)`):

```Dockerfile
hello:
   ARG time=$(date +%H:%M)
   ARG name=John
   RUN echo "hello $name, it is $time"
```

Re-running with the same value makes the `RUN` show as `*cached*`.

## Ways to set a value

1. Command line: `earthly +hello --HELLO=world --FOO=bar`
2. From shell variables: `earthly +hello --HELLO="$HELLO" --FOO="$FOO"`
3. Environment variable `EARTHLY_BUILD_ARGS` (comma separated), handy for args you always want, e.g. kept in `~/.bashrc`:
   ```bash
   export EARTHLY_BUILD_ARGS="HELLO=world,FOO=bar"
   earthly +hello
   ```
4. An `.arg` file, one `name=value` per line (for example `name=eggplant`), then just run `earthly +hello`.

## Variables with LET and SET

`LET` declares a variable that is like a build arg but cannot be used as a parameter (think private/local). `SET` changes it later.

```Dockerfile
hello:
   LET name = "world"
   RUN echo "hello $name"
   SET name = "banana"
   RUN echo "hello $name"
```

Useful when the value depends on an `IF` condition or is built up in a `FOR` loop.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: guides/build-args.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: removed the claim that args are part of the cache hash, which the guide does not state (it only shows the second run as cached).

Method: documentation only; no commands were run.
