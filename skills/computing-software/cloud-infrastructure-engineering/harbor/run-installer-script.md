---
id: computing-software.cloud-infrastructure-engineering.harbor.run-installer-script
name: run-installer-script
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [install-sh, with-trivy, insecure-registry, default-admin, harbor-installer]
level: intro
status: docs-checked
description: "Install Harbor with install.sh, optionally with Trivy, log in with the default admin account, and configure insecure-registries for HTTP."
sources:
  - https://goharbor.io/docs/main/install-config/run-installer-script/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Copy `harbor.yml.tmpl` to `harbor.yml`, configure it and optionally set a storage backend, then install with `install.sh`. The online installer may take time downloading images from Docker Hub.

- Without Trivy (default): `sudo ./install.sh`
- With Trivy: `sudo ./install.sh --with-trivy`

On success, browse to `http://reg.yourdomain.com` (your configured hostname). Unless changed in `harbor.yml`, the default administrator is `admin` with password `Harbor12345`. Create a project such as `myproject`, then:
```sh
docker login reg.yourdomain.com
docker push reg.yourdomain.com/myproject/myrepo:mytag
```

HTTPS installs require the Harbor certificates on the Docker client. HTTP installs require `insecure-registries` in the Docker daemon file (default `/etc/docker/daemon.json`):
```json
{ "insecure-registries": ["myregistrydomain.com:5000", "0.0.0.0"] }
```
After editing it, restart both Docker and Harbor:
1. `systemctl restart docker`
2. `docker compose down -v`
3. `docker compose up -d`

For Trivy behind a web proxy, see the custom CA certificates guide. To secure an HTTP deployment later, follow the HTTPS configuration guide.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Run the Installer Script.
- Removed: an unsupported closing sentence about changing the default password.
Method: documentation only; no commands were run.
