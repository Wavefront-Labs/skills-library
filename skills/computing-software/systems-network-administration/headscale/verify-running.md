---
id: computing-software.systems-network-administration.headscale.verify-running
name: verify-running
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, health, logs, status, verify]
level: intro
status: docs-checked
description: "Confirm a Headscale deployment works: systemd status, container logs, the /health endpoint, headscale health, and internet reachability."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/container.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/official.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/getting-started.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify Headscale is running

## Native install

```
sudo systemctl status headscale
```

## Container

```shell
docker logs --follow headscale
docker ps
curl http://127.0.0.1:8080/health
```

The container health check runs `headscale health`.

## Reachability

The getting-started guide lists as a prerequisite that Headscale is reachable from the Internet, and says to verify this by visiting the health endpoint:

```
curl https://headscale.example.com/health
```


## Config sanity

```
headscale configtest
```

validates the configuration file (configuration page).

## Checked

2026-11-04. Confirmed against the Headscale container install, official releases and getting-started pages (systemctl status, container logs, docker ps, /health, `headscale health` health check, internet-reachability prerequisite). Removed the troubleshooting list and the Gotcha about local versus public reachability, which the pages do not state.

Method: documentation only; no commands were run.
