---
id: computing-software.devops-ci-cd.earthly.earthly-with-docker-basics
name: earthly-with-docker-basics
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, with-docker, pull, load, compose, service, dind, install-dind]
level: practitioner
status: docs-checked
description: "Run docker commands in an Earthly build with WITH DOCKER on an earthly/dind image, using --pull, --load, --compose and --service, and the INSTALL_DIND function."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/docker-in-earthly.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WITH DOCKER basics in Earthly

Goal: run `docker run` and docker-compose inside a build, with an isolated daemon that is started and stopped on demand.

```Dockerfile
hello:
    FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
    WITH DOCKER --pull hello-world
        RUN docker run hello-world
    END
```

- Base on an Earthly-supported dind image: `WITH DOCKER` needs all the Docker binaries, not just the client.
- `WITH DOCKER ... END` starts a daemon and, at the end, terminates it and deletes all its data.
- `--pull IMAGE` fetches the image and stores it in the Earthly cache so a real pull happens only when the image changes. A plain `docker pull` would not, because the daemon cache is cleared after each run.

## Load an image built by Earthly

```Dockerfile
build:
    ...
    SAVE IMAGE my-image:latest

smoke-test:
    FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
    WITH DOCKER --load test:latest=+build
        RUN docker run test:latest
    END
```

`--load +build` (no name) loads the image the target produced.

## docker-compose

```Dockerfile
FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
COPY docker-compose.yml ./
WITH DOCKER \
        --compose docker-compose.yml \
        --service db \
        --service api
    RUN docker run some-integration-test:latest
END
```

`--compose` brings the stack up before the `RUN`, and images the stack needs are added to the pull list automatically, so cache is used efficiently.

## If you cannot use earthly/dind

Earthly will try to install Docker in your image, which caches poorly. Alternative: the UDC `INSTALL_DIND`, which lets you control where the install happens:

```Dockerfile
FROM my-image:latest
DO github.com/earthly/lib+INSTALL_DIND
COPY ./docker-compose.yml ./
WITH DOCKER ...
    ...
END
```

Because the install precedes the `COPY`, it stays cached when `docker-compose.yml` changes.

## Checked

2026-11-07. Read docs/guides/docker-in-earthly.md in full. dind, --pull, --load, --compose/--service and INSTALL_DIND ordering match. Nothing removed.
Method: documentation only; no commands were run.
