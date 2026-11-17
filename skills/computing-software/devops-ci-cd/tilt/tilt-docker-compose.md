---
id: computing-software.devops-ci-cd.tilt.tilt-docker-compose
name: tilt-docker-compose
category: computing-software
field: devops-ci-cd
product: tilt
tags: [docker-compose, tilt]
level: practitioner
status: docs-checked
description: "Run Docker Compose services under Tilt with docker_compose, docker_build, live_update, multiple compose files, and dc_resource labels."
sources:
  - "https://docs.tilt.dev/docker_compose.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Compose with Tilt

Goal: use Docker Compose as the container runtime while organising services from the Tilt dashboard, controlling when each runs, and adding in-place live updates.

## Getting started

Create a Tiltfile at the repo root, then run `tilt up`:

```python
docker_compose("./docker-compose.yml")
```

Unlike `docker-compose up`, Tilt leaves services up when it exits. Turn them down with `tilt down`.

## docker_build

Tilt uses your compose `build` configuration automatically. To use Tilt's updating optimizations, put an image name in docker-compose.yml (e.g. `image: tilt.dev/express-redis-app`; it is not pushed to a registry, so any name will do) and tell Tilt how to build it:

```python
docker_compose('docker-compose.yml')
docker_build('tilt.dev/express-redis-app', '.')
```

Tilt finds the image name in the compose file and uses its own updating strategy.

## live_update

Update the container in place instead of rebuilding:

```python
docker_compose('docker-compose.yml')
docker_build('tilt.dev/express-redis-app', '.',
  live_update = [
    sync('.', '/var/www/app'),
    run('npm i', trigger='package.json'),
    restart_container()
  ])
```

`sync` copies local files into the container, `run` re-runs `npm i` when `package.json` is edited, and `restart_container` restarts the server.

## Multiple compose files

```python
docker_compose(["./docker-compose.yml", "./docker-compose.override.yml"])
```

`docker_compose` also accepts a `blob` for any config item, so overrides can be generated in the Tiltfile, e.g. `docker_compose(["./docker-compose.yml", encode_yaml({'services': overrides})])`, where `overrides` is built from config flags.

## Organizing services

```
dc_resource('redis', labels=["database"])
dc_resource('app', labels=["server"])
dc_resource('storybook', auto_init=False)
```

Labels group services; `auto_init=False` stops a server running at startup. Since Tilt uses Docker Compose to run services, you can use `docker-compose` to examine state outside Tilt.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/docker_compose.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
