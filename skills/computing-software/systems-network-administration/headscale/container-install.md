---
id: computing-software.systems-network-administration.headscale.container-install
name: container-install
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, docker, container, compose, podman, health]
level: practitioner
status: docs-checked
description: "Run Headscale in Docker or Podman: config and lib directories, image sources, published ports, read-only filesystem, health check, and verification."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/container.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/configuration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run Headscale in a container

The container guide is community-written, not maintained by the headscale authors, and may be outdated. Images:

- `docker.io/headscale/headscale:<VERSION>`
- `ghcr.io/juanfont/headscale:<VERSION>`

## Steps

```shell
mkdir -p ./headscale/{config,lib}
cd ./headscale
```

1. Download the example config for your version and save it as `config/config.yaml`; adjust it.
2. Start the container (`docker run` or compose) from within `./headscale`, with these properties from the docs:
   - read-only root filesystem, tmpfs for `/tmp` and `/var/run/headscale` (the compose example mounts only `/var/run/headscale`)
   - `config` mounted read-only at `/etc/headscale`, `lib` at `/var/lib/headscale`
   - ports 8080 and 9090 published on `127.0.0.1` (use `0.0.0.0:8080:8080` instead of `127.0.0.1:8080:8080` to expose externally)
   - health check running `headscale health`
   - command `serve`
   - compose uses `restart: unless-stopped`

## Verify

```shell
docker logs --follow headscale
docker ps
curl http://127.0.0.1:8080/health
```

## Gotchas

- Download the example config for the same version as the image; the `main` branch may contain unreleased changes.
- `docker exec -it` runs commands in an existing container.
- Docker is not an officially supported deployment method (see the FAQ).

## Checked

2026-11-04. Confirmed against the Headscale docs pages for container install, configuration and FAQ (images, directory layout, run options, compose, verify commands). Removed the advice to back up the volume before upgrades, which the page does not give.

Method: documentation only; no commands were run.
