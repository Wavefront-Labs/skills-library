---
id: computing-software.software-engineering.pnpm.docker-official-image
name: docker-official-image
category: computing-software
field: software-engineering
product: pnpm
tags: [docker, ghcr-pnpm-image, official-pnpm-image, buildkit-cache-mount, dev-engines-runtime, docker-image-tags, store-cache-trust]
level: practitioner
status: docs-checked
description: "Use the official ghcr.io/pnpm/pnpm base image: tags, adding pnpm to your own image, letting devEngines.runtime install Node.js, BuildKit cache-mount and hardlink caveats."
sources:
  - https://pnpm.io/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ghcr.io/pnpm/pnpm` is based on `debian:stable-slim` and holds the pnpm standalone binary, the bundled `node-gyp` and needed system libraries. Node.js is NOT bundled. Platforms: `linux/amd64`, `linux/arm64`.

Tags: `<version>` (exact, immutable, includes prereleases), `<major>` (latest stable in the major), `latest` (not moved by prereleases); add `-alpine` for Alpine variants.

Add pnpm to your own image: copy the whole `/opt/pnpm` directory (it contains `node-gyp`), from the image whose C library matches yours, and link `pnpm`, `pn`, `pnpx`, `pnx`:

```dockerfile
FROM node:24-alpine
COPY --from=ghcr.io/pnpm/pnpm:12-alpine /opt/pnpm /opt/pnpm
RUN for bin in pnpm pn pnpx pnx; do ln -s "/opt/pnpm/$bin" "/usr/local/bin/$bin"; done
```

Debian/Ubuntu-based images copy from `ghcr.io/pnpm/pnpm:12`.

Node.js: declare `devEngines.runtime` (`name: node`, `version: 22.x`, `onFail: download`) and `pnpm install` downloads it. Copy `pnpm-workspace.yaml` before installing; omitting it can change installs or break a frozen one.

Caching: hardlinks or reflinks cannot span a container build and the host, so use BuildKit cache mounts. Keep the store cache to mutually trusted builds. A store baked into an image layer is not free to link (overlayfs copies lower-layer files up); `packageImportMethod: copy` is usually faster there.

## Checked

2026-11-04. Confirmed against pnpm.io/docker: base image contents, platforms, tags, /opt/pnpm copy recipe and link names, devEngines.runtime download, pnpm-workspace.yaml copy advice, cache-mount and overlayfs cautions. Removed: the generic closing Check line (a docker run command not on the page).
Method: documentation only; no commands were run.
