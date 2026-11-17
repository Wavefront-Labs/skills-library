---
id: computing-software.cloud-infrastructure-engineering.zot.install-zot-binary-or-container
name: install-zot-binary-or-container
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, install, podman, docker, minimal-image, supported-platforms]
level: intro
status: docs-checked
description: "Get Zot running from a release binary or the full and minimal container images with Podman or Docker, and know which platforms are supported."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot ships as binaries and container images from the project-zot GitHub repository.

Supported platforms: linux/amd64, linux/arm64, darwin/amd64, darwin/arm64, freebsd/amd64 and freebsd/arm64. Container image builds are not supported on FreeBSD.

Run a container (the registry listens on `http://localhost:5000`):

```
podman run -p 5000:5000 ghcr.io/project-zot/zot:latest
podman run -p 5000:5000 ghcr.io/project-zot/zot-minimal:latest
docker run -p 5000:5000 ghcr.io/project-zot/zot:latest
```

- `zot` is the full image with extensions; `zot-minimal` is the core Distribution Spec registry without them.
- Other deployment options: Helm, or a binary run as a systemd service.
- You may rename a downloaded binary to `zot`.

Start from a binary with a config file:

```
zot serve config.yml
```

Recommended extras: install the `zli` command line tool and the `zb` benchmarking tool.

Next step is writing a JSON or YAML configuration file; see the config-file skill.

## Checked

Platform table, image names, run commands and serve command confirmed.

Method: docs-checked 2026-11-09 against zot docs admin-guide/admin-getting-started.md.
