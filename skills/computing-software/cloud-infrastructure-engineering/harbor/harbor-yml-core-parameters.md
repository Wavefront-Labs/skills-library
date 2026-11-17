---
id: computing-software.cloud-infrastructure-engineering.harbor.harbor-yml-core-parameters
name: harbor-yml-core-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [harbor-yml, hostname, https, data-volume, trivy-settings]
level: practitioner
status: docs-checked
description: "Set the required harbor.yml parameters: hostname, http and https ports, certificate paths, admin password, database pool, data_volume and Trivy options."
sources:
  - https://goharbor.io/docs/main/install-config/configure-yml-file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`harbor.yml` (copied from `harbor.yml.tmpl`) holds system-level settings read when you run `install.sh` or `prepare`. Required parameters are uncommented by default.

- `hostname`: IP or FQDN used to reach the portal and registry, for example `reg.yourdomain.com`. Do not use localhost, 127.0.0.1 or 0.0.0.0; the registry must be reachable by external clients.
- `http.port`: default 80. Use HTTP only in air-gapped test or development environments.
- `https.port`: default 443, with `https.certificate` and `https.private_key` as the SSL certificate and key paths. Always use HTTPS in production.
- `internal_tls`: `enabled` and `dir` for TLS between components.
- `harbor_admin_password`: used only on first start; afterwards change it in the portal.
- `database`: local PostgreSQL with `password` (change it for production), `max_idle_conns`, `max_open_conns`, `conn_max_lifetime` and `conn_max_idle_time`. A value of 0 or below means no idle retention, no limit, or never closed.
- `data_volume`: where Harbor data lives; it survives container recreation.
- `trivy`: `ignore_unfixed` (default false), `security_check` (comma list of `vuln`, `config`, `secret`; default `vuln`), `skip_update` (then place `trivy.db` and `metadata.json` manually from `trivy-offline.tar.gz`), `insecure`, and `github_token` to avoid the 60 requests per hour anonymous GitHub limit when downloading the Trivy DB.

The parameters take effect when you run `install.sh` to install or reconfigure Harbor.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Configure the Harbor YML File.
- Removed: the unsupported 'recreate the containers' step.
Method: documentation only; no commands were run.
