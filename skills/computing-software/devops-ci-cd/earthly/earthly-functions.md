---
id: computing-software.devops-ci-cd.earthly.earthly-functions
name: earthly-functions
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, function, do, udc, command, arg-scope, global-arg, reuse]
level: practitioner
status: docs-checked
description: "Define reusable Earthly Functions with FUNCTION and call them with DO, including ARG scoping, global args, and how Functions differ from targets."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly Functions (formerly UDCs)

Goal: reuse a set of instructions across targets. Functions used to be called UDCs (User Defined Commands); the page notes Earthly 0.7 used `COMMAND` where later versions use `FUNCTION`.

## Define and call

Name in ALL_UPPERCASE_SNAKE_CASE; recipe starts with `FUNCTION`:

```Dockerfile
MY_COPY:
    FUNCTION
    ARG src
    ARG dest=./
    ARG recursive=false
    RUN cp $(if $recursive =  "true"; then printf -- -r; fi) "$src" "$dest"
```

```Earthfile
build:
    FROM alpine:3.18
    WORKDIR /function-example
    RUN echo "hello" >./foo
    DO +MY_COPY --src=./foo --dest=./bar
    RUN cat ./bar # prints "hello"
```

A function has no `FROM`: it runs in the build environment of the caller, so it sees `./foo` and its file changes are visible to the caller. Local `COPY` in a function uses the directory of the calling Earthfile.

## ARG scope

Functions have their own `ARG` scope; pass values explicitly with `DO +NAME --key=value`:

```Dockerfile
build:
    ARG var=value-in-build
    DO +PRINT_VAR               # prints "something-else"
    DO +PRINT_VAR --var=$var    # prints "value-in-build"

PRINT_VAR:
    FUNCTION
    ARG var=something-else
    RUN echo "$var"
```

Global imports and global args (`ARG --global a_global_var=value-in-global`) come from the `base` target of the Earthfile where the function is defined, not the one of the caller.

## Functions vs targets

- Targets get build context from their own Earthfile directory; functions inherit it from the caller.
- Functions cannot be run from the `earthly` CLI.
- A function may issue `SAVE ARTIFACT` / `SAVE IMAGE`, but the caller emits the outputs.
- Targets are referenced by `FROM`, `BUILD`, `COPY`, `WITH DOCKER --load`, `FROM DOCKERFILE`; functions only by `DO`. With an import: `DO some-import+MY_FUNCTION`.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: guides/functions.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
