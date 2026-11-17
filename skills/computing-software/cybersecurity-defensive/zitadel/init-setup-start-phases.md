---
id: computing-software.cybersecurity-defensive.zitadel.init-setup-start-phases
name: init-setup-start-phases
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, self-hosting, init, setup, start, migrations]
level: advanced
status: docs-checked
description: "Run ZITADEL's init, setup and start phases separately for fast startup, safe upgrades and scaling."
sources:
  - https://zitadel.com/docs/self-hosting/manage/updating_scaling
  - https://zitadel.com/docs/self-hosting/manage/cli/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL has three phases. For a quick start, `zitadel start-from-init` combines them. For day-two operations, run `zitadel init` and `zitadel setup` separately and then `zitadel start`.

- Init: prepares the database connection. It runs once over the full life cycle, before the first setup. It needs a PostgreSQL superuser to create the unprivileged database user and the database if they do not exist; later phases connect as the unprivileged user only.
- Setup: runs each time a new version is deployed. It handles database migrations and picks up changes such as ExternalDomain, ExternalPort and ExternalSecure. It requires only the user created by init.
- Start: the runtime phase, which accepts traffic immediately.

`zitadel start-from-setup` runs setup then the server, and `start-from-init` runs init, setup, then the server.

Both init and setup are idempotent, so running them more often does not change state unexpectedly.

The ZITADEL binary is stateless because all shared state is in the database, so you can run as many instances in parallel as you want. Splitting the phases shortens startup, which matters for scale-to-zero platforms such as Knative or Google Cloud Run. The official Helm chart already runs init and setup as Kubernetes Jobs.

## Checked
2026-11-08. Confirmed against the ZITADEL Update and Scale page and the CLI overview: phase roles, superuser need in init, setup-only privileges, start-from-init and start-from-setup, idempotency (with the same binary version), stateless binary, scale to zero, Helm chart Jobs. Fixed the source URL list.
Method: documentation only; no commands were run.
