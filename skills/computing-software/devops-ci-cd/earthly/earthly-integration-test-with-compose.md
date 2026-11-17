---
id: computing-software.devops-ci-cd.earthly.earthly-integration-test-with-compose
name: earthly-integration-test-with-compose
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, integration-testing, with-docker, compose, smoke-test, docker-compose, build]
level: practitioner
status: docs-checked
description: "Run integration and smoke tests against docker-compose dependencies in an Earthly target using WITH DOCKER --compose, waiting for the DB, and chain them with an all target."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/integration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Integration tests with WITH DOCKER --compose

Goal: reuse a service docker-compose file so integration tests run the same locally and in CI.

Base image used by the guide (a Scala example, but the pattern is stack-independent):

```Dockerfile
VERSION 0.8
FROM earthly/dind:alpine-3.19-docker-25.0.5-r0
WORKDIR /scala-example
RUN apk add openjdk11 bash wget postgresql-client
```

## In-app integration test

Copy source and the compose file, then run the tests inside `WITH DOCKER --compose`. Wait for the database first:

```Dockerfile
integration-test:
    FROM +project-files
    COPY src src
    COPY docker-compose.yml ./
    WITH DOCKER --compose docker-compose.yml
        RUN while ! pg_isready --host=localhost --port=5432 --dbname=iso3166 --username=postgres; do sleep 1; done ;\
            sbt it:test
    END
```

Run it with `earthly -P +integration-test`. A failure in CI can be reproduced locally the same way.

## End-to-end smoke test

Also load the built image with `--load=+docker` and run a script that starts it:

```dockerfile
smoke-test:
    FROM +project-files
    COPY docker-compose.yml ./
    COPY src/smoketest ./
    WITH DOCKER --compose docker-compose.yml --load=+docker
        RUN while ! pg_isready --host=localhost --port=5432 --dbname=iso3166 --username=postgres; do sleep 1; done ;\
            ./smoketest.sh
    END
```

## Tie it together

```Dockerfile
all:
  BUILD +build
  BUILD +unit-test
  BUILD +integration-test
  BUILD +smoke-test
```

`earthly -P +all` runs everything.

## Gotcha

All of the guide examples run `earthly -P` for targets using `WITH DOCKER`.

## Checked

2026-11-07. Read docs/guides/integration.md in full. The Earthfile targets, WITH DOCKER --compose, smoke test, all target and earthly -P usage match. The external Full file Earthfile links on the page were not opened. Nothing removed.
Method: documentation only; no commands were run.
