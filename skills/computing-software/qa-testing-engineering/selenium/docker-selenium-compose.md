---
id: computing-software.qa-testing-engineering.selenium.docker-selenium-compose
name: docker-selenium-compose
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [docker-selenium, selenium-docker, docker-compose-grid, node-chrome]
level: practitioner
status: docs-checked
description: "Run Selenium Grid with docker-selenium images (standalone-chrome, hub, node-*) via docker compose: shm size, env config, scaling nodes and pinning image tags."
sources:
  - https://github.com/SeleniumHQ/docker-selenium
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/README.md
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/ENV_VARIABLES.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker-selenium images and docker compose

## Standalone container
```bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size=2g selenium/standalone-chrome:<tag>
```
- `--shm-size="2g"` is the documented workaround for browsers crashing in containers (arbitrary value; tune it).
- Port 7900: noVNC in the browser (password `secret` by default) to watch sessions; VNC clients use 5900.

## Compose hub + nodes
```yaml
services:
  selenium-hub:
    image: selenium/hub:<tag>
    ports: ["4442:4442", "4443:4443", "4444:4444"]
  chrome:
    image: selenium/node-chrome:<tag>
    shm_size: 2gb
    depends_on: [selenium-hub]
    environment:
      SE_EVENT_BUS_HOST: selenium-hub
      SE_EVENT_BUS_PUBLISH_PORT: 4442
      SE_EVENT_BUS_SUBSCRIBE_PORT: 4443
      SE_NODE_MAX_SESSIONS: 2
      SE_NODE_OVERRIDE_MAX_SESSIONS: "true"
  firefox:
    image: selenium/node-firefox:<tag>
    shm_size: 2gb
    depends_on: [selenium-hub]
    environment: { SE_EVENT_BUS_HOST: selenium-hub, SE_EVENT_BUS_PUBLISH_PORT: 4442, SE_EVENT_BUS_SUBSCRIBE_PORT: 4443 }
```
Scale: `docker compose up -d --scale chrome=4`.

## Useful env vars
`SE_NODE_SESSION_TIMEOUT` (idle session kill, default 300), `SE_SESSION_REQUEST_TIMEOUT` (queue wait, default 300), `SE_NODE_MAX_SESSIONS` (default 1), `SE_SCREEN_WIDTH`/`SE_SCREEN_HEIGHT` (1920x1080), `SE_VNC_NO_PASSWORD`, `SE_START_VNC`, `SE_OPTS` (extra CLI flags without their own variable), `TZ` (time zone).

## Tags
Always use a full tag (for example `4.51.0-20261010`: Grid version plus build date) to pin the browser and Grid version. Images are multi-arch for amd64 and aarch64 (armhf is unsupported); Edge is amd64 only, and older Chrome versions are amd64 only (Chrome images use the Chromium driver on ARM64).

## App under test
The browser runs inside the container, so `localhost` means the container. Use the compose service name (`http://web:3000`) for apps in the same compose network.

## Gotchas
- Tests can start before nodes register: poll the Grid status first. The images include `/opt/bin/check-grid.sh` for use as a container health check.

## Verify
`curl localhost:4444/status` shows chrome and firefox slots; tests pass against `http://localhost:4444`.

## Checked

Checked 2026-10-25 against the docker-selenium repository (pushed 2026-10-20; README, ENV_VARIABLES.md, images 4.51.0-20261010). Confirmed: image names, ports 4442/4443/4444/7900/5900, `--shm-size`, noVNC password `secret`, every `SE_*` variable in the examples and list with its default, the full-tag recommendation, the multi-arch table, `check-grid.sh` health check. Corrected: the tag format example; ARM note expanded. Removed: the `-v /dev/shm:/dev/shm` alternative, `host.docker.internal` for apps (only documented for the Docker daemon URL) and the run-client-in-compose advice.

Method: documentation only; no commands were run.
