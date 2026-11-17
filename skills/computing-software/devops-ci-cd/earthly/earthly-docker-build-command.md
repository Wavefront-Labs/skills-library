---
id: computing-software.devops-ci-cd.earthly.earthly-docker-build-command
name: earthly-docker-build-command
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, docker-build, dockerfile, tag, target, platform, push, satellite]
level: practitioner
status: docs-checked
description: "Build an image from a plain Dockerfile with earthly docker-build, using --dockerfile, repeatable --tag, --target and multiple --platform values, plus --push."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# earthly docker-build

Goal: build a Docker image from a Dockerfile instead of an Earthfile, with Earthly caching and runners.

```
earthly [options] docker-build [--dockerfile <dockerfile-path>] [--tag=<image-tag>] [--target=<target-name>] [--platform <platform1[,platform2,...]>] <build-context-dir> [--arg1=arg-value]
```
`<build-context-dir>` is the directory of the Dockerfile build context; by default a file named `Dockerfile` is expected in it.

## Examples
Build using the `myDockerfiles` directory as the context:
```
earthly docker-build --dockerfile Dockerfile ./myDockerfiles
```
Push an image built for linux/arm64:
```
earthly docker-build --dockerfile Dockerfile --platform linux/arm64 --tag {DOCKER_TAG} --push ./myDockerfiles
```
Use a satellite runner:
```
earthly docker-build --sat my-satellite --tag my-image:latest .
```

## Options
- `--dockerfile <dockerfile-path>`: alternative Dockerfile.
- `--tag=<image-tag>`: image name and tag; repeat the option to give the image several tags.
- `--target=<target-name>`: target to build in a multi-target Dockerfile.
- `--platform <platform1[,platform2,...]>`: platform(s) to build for.

## Gotchas
- Unlike a regular earthly build, `docker-build` accepts multiple platforms in `--platform`.
- All other build options (such as `--push`) are supported; see the build options.

## Notes
Build args for the Dockerfile are passed after the context directory in the synopsis form `[--arg1=arg-value]`. The `{DOCKER_TAG}` in the push example is the docs placeholder for your image tag. A satellite is a remote runner; see the satellite commands skill for creating one.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
