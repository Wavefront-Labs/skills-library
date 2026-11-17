---
id: computing-software.cloud-infrastructure-engineering.harbor.trivy-custom-ca-certificates
name: trivy-custom-ca-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [trivy, custom-ca, web-proxy, trivy-adapter, harbor-cust-cert]
level: advanced
status: docs-checked
description: "Give the Harbor Trivy adapter a custom CA bundle for enterprise web proxies by using the trust-certificates mount, and keep it across upgrades."
sources:
  - https://goharbor.io/docs/main/administration/vulnerability-scanning/configure-custom-certs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy must reach the internet to fetch CVE data. Behind an enterprise web proxy that re-signs TLS, you must give Trivy your proxy CA. You need the CA bundle or single public certificates.

Procedure:
1. Change into the Harbor configuration folder and look at the `trivy-adapter` service in `docker-compose.yml`. It has a bind mount with `target: /harbor_cust_cert` and, by default, `source: ./common/config/shared/trust-certificates`.
2. Copy your CA bundle or certificates into that source folder.
3. Optionally change the host path in the compose file. You then have to maintain that change across releases.
4. Restart: `docker restart trivy-adapter` or `docker compose restart`. If you changed the bind path, run `docker compose up -d` instead.

Upgrades may overwrite the folder or a mount from a different location, so:
1. Back up your certificates to a folder unrelated to the Harbor configuration.
2. Upgrade Harbor as usual.
3. Confirm the `/harbor_cust_cert` mount still points to the folder holding your certificates (normally `./common/config/shared/trust-certificates`).
4. If the folder is empty, copy the backed-up certificates back.
5. Check that Trivy can fetch CVE data.

## Checked

2026-11-03. Mount target, default source folder, restart commands and the upgrade procedure were read against the Harbor docs page Configure custom Certification Authorities for trivy. Nothing removed.

Method: documentation only; no commands were run.
