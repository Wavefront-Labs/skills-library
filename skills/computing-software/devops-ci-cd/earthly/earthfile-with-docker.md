---
id: computing-software.devops-ci-cd.earthly.earthfile-with-docker
name: earthfile-with-docker
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, with-docker, pull, load, compose, service, dind]
level: practitioner
status: docs-checked
description: "Run containers inside an Earthfile with WITH DOCKER ... END, loading images via --pull, --load, --compose and --service on a temporary Docker daemon."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WITH DOCKER

Goal: run docker commands (integration tests, compose stacks) during a build.

```Dockerfile
FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
WORKDIR /test
COPY docker-compose.yml ./
WITH DOCKER \
        --compose docker-compose.yml \
        --load image-name:latest=(+some-target --SOME_BUILD_ARG=value) \
        --load another-image-name:latest=+another-target \
        --pull some-image:latest
    RUN docker run ... && \
        docker run ... && \
        ...
END
```

## Rules
- `WITH DOCKER` starts a Docker daemon for one `RUN`; afterwards the daemon and its data (volumes, networks) are deleted, but other created files are kept.
- It implies `RUN --privileged`.
- Only a single `RUN` is permitted inside; chain commands with `;` or `&&`. Do other commands (such as `COPY`) before or after the block.
- `--load` targets are built in parallel; `--pull` images download in parallel.
- Use an image that already has `dockerd` for speed; otherwise Earthly tries to install it. Officially supported: `earthly/dind:alpine-3.19-docker-25.0.5-r0` and `earthly/dind:ubuntu-23.04-docker-25.0.2-1`.
- In a `LOCALLY` target no cleanup happens afterwards, so use `RUN docker run --rm ...`.

## Options
- `--pull <image-name>`: pull from a registry into the temp daemon (repeatable). Prefer it over `RUN docker pull`, which ignores Earthly caching.
- `--load [<image-name>=]<target-ref>`: build the target's image and load it; referenced by `<image-name>` or by the name in the target's `SAVE IMAGE`. Build args go in parentheses. It does not mark outputs or pushes; use `BUILD`.
- `--compose <compose-file>`: load the compose definition, pull its images and start services; repeatable like `docker-compose -f`.
- `--service <compose-service>`: start only the named services; requires `--compose`; repeatable.
- `--platform <platform>`: platform for `--load` and `--pull` images.
- `--allow-privileged`: same as for FROM.
- `--build-arg` is deprecated; use `--load <image-name>=(<target-ref> --<key>=<value>)`.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
