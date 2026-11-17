---
id: computing-software.devops-ci-cd.verdaccio.docker-plugins-and-compose
name: docker-plugins-and-compose
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [docker-plugins, docker-compose, multi-stage, plugin-image, docker-compose-yaml, multi-stage-build, verdaccio-plugins]
level: advanced
status: docs-checked
description: "Add plugins to the Verdaccio Docker image by multi-stage build or by mounting /verdaccio/plugins, and run the registry with docker-compose named volumes."
sources:
  - https://verdaccio.org/docs/docker/
  - https://verdaccio.org/docs/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Verdaccio looks in `/verdaccio/plugins` at startup. Build plugins with native dependencies on the same base image as the Verdaccio Dockerfile.

Multi-stage image:
```
FROM node:lts-alpine as builder
RUN mkdir -p /verdaccio/plugins \
  && cd /verdaccio/plugins \
  && npm install --install-strategy=shallow --no-bin-links --omit=optional verdaccio-auth-memory@latest
FROM verdaccio/verdaccio:6
ADD docker.yaml /verdaccio/conf/config.yaml
COPY --chown=$VERDACCIO_USER_UID:root --from=builder \
  /verdaccio/plugins/node_modules/verdaccio-auth-memory \
  /verdaccio/plugins/verdaccio-auth-memory
```
Alternatively mount a plugins volume with `-v $V_PATH/plugins:/verdaccio/plugins`.

docker-compose:
```yaml
services:
  verdaccio:
    image: verdaccio/verdaccio
    ports: ['4873:4873']
    environment:
      - VERDACCIO_PORT=4873
    volumes:
      - verdaccio_storage:/verdaccio/storage
      - verdaccio_conf:/verdaccio/conf
      - verdaccio_plugins:/verdaccio/plugins
volumes:
  verdaccio_storage:
  verdaccio_conf:
  verdaccio_plugins:
```
Run `docker-compose up --build`; prefix with `VERDACCIO_PORT=5000` to change the port. Find the host location with `docker volume inspect verdaccio_conf`.

## Checked

2026-11-04. Confirmed against the Verdaccio Docker page (Plugins section, multi-stage Dockerfile, volume mount, docker-compose volumes, VERDACCIO_PORT prefix, docker volume inspect). Nothing removed.
Method: documentation only; no commands were run.
