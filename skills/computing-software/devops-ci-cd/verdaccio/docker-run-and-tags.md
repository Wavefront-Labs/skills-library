---
id: computing-software.devops-ci-cd.verdaccio.docker-run-and-tags
name: docker-run-and-tags
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [docker, docker-image, tags, docker-hub, image-tags, nightly, verdaccio-verdaccio]
level: intro
status: docs-checked
description: "Run the official verdaccio/verdaccio image, pin versions by tag (6, 6.10, 6.10.3), nightly 6.x-next and 7.x-next builds, and build your own image."
sources:
  - https://verdaccio.org/docs/docker/
  - https://verdaccio.org/docs/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
docker pull verdaccio/verdaccio
docker run -it --rm --name verdaccio -p 4873:4873 verdaccio/verdaccio
```
Add `-d` to run in the background. Tags: `latest` points at the current stable release (6.x at time of writing) and will move to the next stable line; pin at least the major in production.

```
docker pull verdaccio/verdaccio:6        # latest 6.x
docker pull verdaccio/verdaccio:6.10     # latest 6.10.x
docker pull verdaccio/verdaccio:6.10.3   # exact release
```
Nightly images rebuilt from branch tips (not production-ready): `6.x-next`, `7.x-next`.

Build locally:
```
docker build -t verdaccio .
```
(or the `build:docker` script run through yarn or pnpm); the first build takes minutes and repeats when files outside `.dockerignore` change. Use `verdaccio` as the image name for a local build.

The repository `docker-examples/` folder has runnable examples (local storage, nginx and Apache proxies, local plugin image, S3 storage, GitHub OAuth, Helm, stage and tfa flags) grouped by v7, v6 and v9 (experimental). The pages disagree on which line is stable: the Docker page says `latest` is 6.x yet its examples table calls v7 current stable, and the Kubernetes page calls v6 the current stable line and v7 the next major. Check the Docker Hub tag list before pinning.

Verify: the endpoint `/-/ping` on port 4873 (the Docker page uses it for its health check; the image declares no HEALTHCHECK itself).

## Checked

2026-11-04. Read the Verdaccio documentation pages: Docker and Installation. Confirmed: the pull and run commands, the latest tag pointing at 6.x, the 6, 6.10 and 6.10.3 tags, the nightly 6.x-next and 7.x-next tags, docker build, the build:docker script, and the docker-examples contents. Removed or corrected: the curl check (the page only shows /-/ping inside a health check); the docs disagree on which line is stable, noted in the skill.

Method: documentation only; no commands were run.
