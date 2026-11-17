---
id: computing-software.devops-ci-cd.earthly.earthly-with-docker-compose
name: earthly-with-docker-compose
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, with-docker, docker-compose, dind, allow-privileged, load, pull, integration-tests]
level: practitioner
status: docs-checked
description: "Run Docker inside an Earthly target with WITH DOCKER, using --pull, --load and --compose on the earthly/dind image, and run it with --allow-privileged."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/basics/part-6-using-docker-with-earthly.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WITH DOCKER, --load and --compose

Goal: run docker commands (or docker-compose services) inside a target, for example integration tests.

`WITH DOCKER` starts a Docker daemon usable by the `RUN` inside its block, which ends with `END`. The docs recommend (not require) Earthly's dind image `earthly/dind:alpine-3.19-docker-25.0.5-r0`.

## Pull an image
```Dockerfile
hello:
    FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
    WITH DOCKER --pull hello-world
        RUN docker run hello-world
    END
```

## Load an image built by another target
```Dockerfile
my-hello-world:
    FROM ubuntu
    CMD echo "hello world"
    SAVE IMAGE my-hello:latest

hello:
    FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
    WITH DOCKER --load hello:latest=+my-hello-world
        RUN docker run hello:latest
    END
```
Loading does not run the image; you must run it explicitly.

## Compose services plus a test image
```Dockerfile
integration-tests:
    FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
    COPY docker-compose.yml ./
    WITH DOCKER --compose docker-compose.yml --load tests:latest=+test-setup
        RUN docker run --network=default_go/part6_default tests:latest
    END
```
`--compose` makes Earthly start the services defined in the compose file. Here `+test-setup` is a separate target that copies in the tests and sets the test command as its `ENTRYPOINT`, saved as an image.

Run it with the privileged flag:

```bash
earthly --allow-privileged +integration-tests
```
`-P` is the short form (the JS example runs `earthly -P +app-with-api`). Multiple `--load` flags can be given in one `WITH DOCKER`.

## Gotcha
The compose network name in the example (`default_go/part6_default`) comes from that example's compose file; adjust it to your own network. The Java and Python examples wait for Postgres with `pg_isready` in the `RUN` before starting the container.

## Checked

2026-11-07. Read the Part 6 basics page (docs/basics) in full, including the JS, Java and Python tab text. dind recommendation, --pull, --load, --compose, -P, pg_isready and network naming match. Nothing removed.
Method: documentation only; no commands were run.
