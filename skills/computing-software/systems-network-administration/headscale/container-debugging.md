---
id: computing-software.systems-network-administration.headscale.container-debugging
name: container-debugging
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, debug-image, distroless, busybox, docker-exec, container]
level: practitioner
status: docs-checked
description: "Get a shell inside the Headscale container using the -debug image variant, since the default image is distroless, and find the binary path."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/container.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging the Headscale container

The default image is distroless: no shell or other debug tools. Use the `-debug` variant (for example `docker.io/headscale/headscale:x.x.x-debug`), which includes a minimalist Busybox shell. Use the exact same run commands as for the normal image with the tag swapped (x.x.x is the headscale version); the two containers are compatible, so you can alternate between them:

```shell
docker run -it docker.io/headscale/headscale:x.x.x-debug sh
docker run docker.io/headscale/headscale:x.x.x-debug ls /ko-app
```

The default command in the debug container runs `headscale`, which is located at `/ko-app/headscale`.

Using `docker exec -it` runs commands in an existing container.

## Notes

- The container guide is community-maintained. The FAQ says Docker is not an officially supported deployment method and points to the "docker-issues" channel on the Discord server for community help.

## Checked

2026-11-04. Confirmed against the Headscale container install page (debug variant section) and the FAQ. Removed the advice to keep the debug image out of production and the `docker exec ... headscale --help` and logs/curl tips, none of which the debugging section states.

Method: documentation only; no commands were run.
