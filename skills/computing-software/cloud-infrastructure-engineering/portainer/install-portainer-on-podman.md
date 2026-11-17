---
id: computing-software.cloud-infrastructure-engineering.portainer.install-portainer-on-podman
name: install-portainer-on-podman
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [install, podman, socket, docker-compatible-api]
level: practitioner
status: docs-checked
description: "Install Portainer Server on Podman on Linux through the Docker-compatible API socket, including the supported platform and the privileged flag."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/start/install/server/podman/linux.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Portainer manages Podman through Podman's Docker-compatible API, not a native integration. Podman environments therefore behave like Docker environments, and support is limited to configurations where that compatibility layer behaves consistently. The documented supported platform is CentOS 9 with Podman 5.x; other versions and distros may work but are not supported. Run Podman as root; rootless may work but is not officially supported.

Steps:

```
systemctl enable --now podman.socket
podman volume create portainer_data
podman run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always \
  --privileged -v /run/podman/podman.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ee:lts
```

The Podman socket is mapped to the path Portainer expects for Docker, and the container runs with `--privileged`. As elsewhere, 9443 serves the UI and 8000 is only for the Edge tunnel. A license key is needed for Business Edition.

As on Docker, the first-time setup then asks for the admin user and setup token (see the server logs with `podman logs portainer`), and later environments are added through the Environment Wizard.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
