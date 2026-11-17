---
id: computing-software.cloud-infrastructure-engineering.portainer.install-portainer-server-on-docker-linux
name: install-portainer-server-on-docker-linux
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [install, docker, linux, ports, volumes, selinux]
level: practitioner
status: docs-checked
description: "Install Portainer Server on Docker Standalone on Linux with docker run or Compose, including the ports, data volume, certificate and SELinux notes."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/start/install/server/docker/linux.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: a working current Docker engine (the docs advise against the snap package on Ubuntu), sudo on the host, and a license key if installing Business Edition. Portainer Server exposes the UI on port 9443 and an optional TCP tunnel server on 8000; 8000 is only needed for Edge agents.

Create the data volume, then run the container (this is the Business Edition image shown by the docs):

```bash
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ee:lts
```

A Docker Compose file is also provided and is downloaded with curl from the Portainer downloads site.

Port 9443 uses a self-signed certificate by default. You can supply your own certificate at install time or later in the UI settings. Add `-p 9000:9000` only if you still need legacy HTTP on 9000.

Assumptions in the instructions: Docker is reached over the Unix socket, Docker runs as root (rootless needs extra configuration), and SELinux is disabled. If you need SELinux, pass `--privileged` to Docker when deploying Portainer.

New instances require a setup token for first-time setup; a startup flag skips or customizes it. Confirm the container is up with `docker ps`.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
