---
id: computing-software.database-administration.dragonfly.http-access-and-auth
name: http-access-and-auth
category: computing-software
field: database-administration
product: dragonfly
tags: [http-api, requirepass, admin-nopass, primary-port-http-enabled, expose-http-api]
level: practitioner
status: docs-checked
description: "Control Dragonfly's HTTP console: disable it on the main port, authenticate with requirepass, and know that /metrics bypasses auth."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/using-http.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly serves HTTP for certain operations on the same TCP port as Redis (6379) by default. If `--admin_port` is set it also serves HTTP on the admin port.

Controls:

- Disable on the main port: `--primary_port_http_enabled=false` (default true).
- `--expose_http_api` (default false) exposes a POST `/api` handler that accepts Redis commands as a JSON array.

## Authentication

- By default HTTP needs no authentication.
- If `requirepass` is set, HTTP requests authorise with username `default` and the `requirepass` value.
- This `default` is not the ACL `default` user. They need not share a password: `ACL SETUSER default >newpass` does not change `requirepass`.
- If `admin_nopass` is set it bypasses `requirepass` on the admin port, so all requests to that port need no authentication.

## Metrics page

The `/metrics` page **always bypasses auth**, so anyone who can reach the port can read it. Restrict network access (bind address, firewall, or the admin port) if metrics are sensitive.

`--admin_bind` binds the admin console to a given address and `--bind` limits the main listener; an empty `bind` listens on all interfaces, which is not advised.

## Checked

2026-11-04. Confirmed in the HTTP page (main port, `primary_port_http_enabled`, admin port, authentication, `/metrics` bypass) and the flags page (`expose_http_api`, `admin_bind`, `bind`, `admin_nopass` and defaults). Nothing removed.

Method: documentation only; no commands were run.
