---
id: computing-software.devops-ci-cd.earthly.earthly-pass-args-and-matrix
name: earthly-pass-args-and-matrix
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, arg, build, pass-args, matrix-builds, copy, with-docker, dynamic-args]
level: practitioner
status: docs-checked
description: "Pass build args between Earthly targets and Earthfiles, use --pass-args, repeat an arg for a matrix build, and set dynamic values with a dollar-paren shell expression."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/build-args.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Passing args to targets and matrix builds in Earthly

Goal: give a called target its `ARG` values, and fan one target out over several values.

## Passing to a target

```Dockerfile
greeting:
   BUILD +hello --name=world

hello:
    ARG name
    RUN echo "hello $name"
```

Within the same Earthfile, command-line overrides flow through automatically: running `earthly +greeting --name=world` passes `--name=world` to `+hello` even if `BUILD +hello` carries no args.

That automatic pass does not apply to references to other Earthfiles. Either pass explicitly:

```Dockerfile
ARG name
BUILD +hello --name=$name
```

or pass everything with the `--pass-args` flag:

```Dockerfile
BUILD --pass-args +hello
```

## Matrix builds

Giving the same arg several values makes Earthly build the target once per value:

```dockerfile
greetings:
    BUILD +hello \
        --name=world \
        --name=banana \
        --name=eggplant
```

`earthly +greetings` then runs `+hello` three times.

## Where args can be given

Args can follow `BUILD`, `FROM`, `COPY`, and `WITH DOCKER --load`, among others:

```Dockerfile
BUILD +hello --name=world
COPY (+hello/file.txt --name=world) ./
FROM +hello --name=world
WITH DOCKER --load=(+hello --name=world)
  ...
END
```

## Dynamic values

A value in `$(...)` is the output of a shell command: `BUILD +hello --name=$(echo world)` sets `name` to `world`.

## Checked

2026-11-07. Read docs/guides/build-args.md in full. Automatic passing within an Earthfile, explicit passing and --pass-args across Earthfiles, matrix builds, commands accepting args and $(...) values match. Nothing removed.
Method: documentation only; no commands were run.
