---
id: computing-software.qa-testing-engineering.selenium.dynamic-grid-docker
name: dynamic-grid-docker
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [dynamic-grid, docker-node, ephemeral-browser-containers, selenium-grid]
level: practitioner
status: docs-checked
description: "Configure Selenium Dynamic Grid so each session gets a fresh browser container via node-docker: TOML configs, image mapping, video and Docker socket security."
sources:
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/README.md
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/docker-compose-v3-dynamic-grid.yml
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/ENV_VARIABLES.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic Grid with Docker

**Goal:** a clean browser container per test session, started on demand and removed afterwards.

## config.toml for node-docker
```toml
[docker]
configs = [
  "selenium/standalone-chrome:<tag>", '{"browserName": "chrome"}',
  "selenium/standalone-firefox:<tag>", '{"browserName": "firefox"}',
  "selenium/standalone-edge:<tag>", '{"browserName": "MicrosoftEdge"}'
]
url = "http://127.0.0.1:2375"      # docker daemon API (or unix socket via mounted socket)
video-image = "selenium/video:<tag>"
host-config-keys = ["Dns", "DnsOptions", "DnsSearch", "ExtraHosts", "Binds"]

[node]
session-timeout = 300
override-max-sessions = true
max-sessions = 8
```

## Compose
```yaml
  node-docker:
    image: selenium/node-docker:<tag>
    volumes:
      - ./assets:/opt/selenium/assets          # videos and logs per session
      - ./config.toml:/opt/selenium/docker.toml
      - /var/run/docker.sock:/var/run/docker.sock
    environment: { SE_EVENT_BUS_HOST: selenium-hub, SE_EVENT_BUS_PUBLISH_PORT: 4442, SE_EVENT_BUS_SUBSCRIBE_PORT: 4443 }
```
Child containers receive every `SE_`-prefixed environment variable set on the `node-docker` or `standalone-docker` container (for example `SE_NODE_SESSION_TIMEOUT`). Mount the file at `/opt/selenium/docker.toml` (the default name for `node-docker`, `SE_NODE_DOCKER_CONFIG_FILENAME=docker.toml`) so it does not clash with the `config.toml` that browser containers use.

## Per-session capabilities
`se:recordVideo: true`, `se:screenResolution: "1920x1080"`, `se:timeZone: "US/Pacific"` (the README example), `se:name` (used in the video file name).

## Security
Mounting the Docker socket gives broad control of the host Docker daemon. Run on dedicated CI hosts, not shared machines.

## Gotchas
- The app under test must be reachable from the browser containers; check the network settings for your Docker setup.
- Maximum concurrent containers are limited by `max-sessions`; queued requests wait up to `session-request-timeout`.

## Verify
`docker ps` shows a new standalone container per running test, removed when the session ends; videos and session information appear in the mounted `./assets` folder.

## Checked

Checked 2026-10-25 against the docker-selenium README (Dynamic Grid section; pushed 2026-10-20, images 4.51.0-20261010) and ENV_VARIABLES.md. Confirmed: `[docker]` keys `configs`, `url`, `video-image`, `host-config-keys`, the `/var/run/docker.sock` mount with the 127.0.0.1:2375 URL, `/opt/selenium/assets`, the capabilities `se:recordVideo`, `se:screenResolution`, `se:timeZone`, `se:name`, forwarding of `SE_` variables to child containers. Corrected: the config mount path is `/opt/selenium/docker.toml`, not `config.toml`; `host-config-keys` entries are Docker host config keys such as `Binds`, not `ShmSize`. Removed: the pre-pull advice, the rootless Docker suggestion and the undocumented `[docker] network` key.

Method: documentation only; no commands were run.
