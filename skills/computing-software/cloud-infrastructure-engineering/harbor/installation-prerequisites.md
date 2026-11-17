---
id: computing-software.cloud-infrastructure-engineering.harbor.installation-prerequisites
name: installation-prerequisites
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [prerequisites, system-requirements, docker-compose, ports, harbor]
level: intro
status: docs-checked
description: "Check Harbor host requirements before install: CPU, memory and disk, Docker and Compose versions, ports 80 and 443, and the Helm alternative."
sources:
  - https://goharbor.io/docs/main/install-config/installation-prereqs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor deploys to a Docker host with Docker Compose, or to Kubernetes with Helm. For Kubernetes, use the dedicated harbor-helm repository (github.com/goharbor/harbor-helm); this prerequisites page covers the Compose host.

Resources:
- CPU: minimum 2, recommended 4
- Memory: minimum 4 GB, recommended 8 GB
- Disk: minimum 40 GB, recommended 160 GB

Software on the target host:
- Docker Engine: version above 20.10
- Docker Compose: above 2.3 (part of Docker Engine)
- OpenSSL: latest, optional, for generating certificates and keys

Network ports that must be open:
- 443, HTTPS: portal and core API. Changeable in the configuration file.
- 80, HTTP: portal and core API. Changeable in the configuration file.

Next step after meeting these: download the Harbor installer, then configure `harbor.yml` and run `install.sh`.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Harbor Installation Prerequisites.
- Removed: an unsupported paragraph about changing ports instead of freeing them.
Method: documentation only; no commands were run.
