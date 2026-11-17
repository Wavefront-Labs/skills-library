---
id: computing-software.devops-ci-cd.verdaccio.docker-env-port-https-health
name: docker-env-port-https-health
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [docker-env, healthcheck, docker-port, verdaccio-port, verdaccio-protocol, docker-healthcheck, ping]
level: practitioner
status: docs-checked
description: "Change port and protocol in Docker with VERDACCIO_PORT and VERDACCIO_PROTOCOL, and add a /-/ping HEALTHCHECK using 127.0.0.1 because the image has none."
sources:
  - https://verdaccio.org/docs/docker/
  - https://verdaccio.org/docs/env/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `listen` setting in `conf/config.yaml` is ignored in Docker. Use variables:

```
docker run -it --rm --name verdaccio -e "VERDACCIO_PORT=8080" -p 8080:8080 verdaccio/verdaccio
docker run -it --rm --name verdaccio --env "VERDACCIO_PROTOCOL=https" -p 4873:4873 verdaccio/verdaccio
```
Ports in `-p` must match. For HTTPS, specify the certificates in `config.yaml` first. Other variables: `VERDACCIO_APPDIR` (/opt/verdaccio), `VERDACCIO_USER_NAME` (verdaccio), `VERDACCIO_USER_UID` (10001), `VERDACCIO_ADDRESS` (7.x `[::]`, 6.x `0.0.0.0`; set `0.0.0.0` where IPv6 is unavailable).

The image declares no `HEALTHCHECK`. Probe `/-/ping` with 127.0.0.1 (Alpine resolves `localhost` to `::1` first, while Verdaccio listens on IPv4 by default):

```
--health-cmd 'wget --quiet --tries=1 --spider http://127.0.0.1:4873/-/ping || exit 1' \
--health-interval 30s --health-timeout 5s --health-start-period 10s --health-retries 3
```
The same `test: ['CMD-SHELL', 'wget ...']` works in docker-compose. Adjust the URL if you changed the port or protocol. Busybox wget cannot skip certificate validation, so with a self-signed cert probe through Node with `NODE_TLS_REJECT_UNAUTHORIZED=0 node -e "fetch(...)"`.

## Checked

2026-11-04. Confirmed against the Verdaccio Docker page (port, protocol, health check, wget and Node probes, Alpine localhost note) and the Environment Variables page (variable defaults). Removed: the generic closing Verify tip.
Method: documentation only; no commands were run.
