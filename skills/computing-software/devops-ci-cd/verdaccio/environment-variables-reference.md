---
id: computing-software.devops-ci-cd.verdaccio.environment-variables-reference
name: environment-variables-reference
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [environment-variables, verdaccio-public-url, forwarded-proto, verdaccio-storage-path, verdaccio-handle-kill-signals, verdaccio-forwarded-proto, env-vars]
level: practitioner
status: docs-checked
description: "Reference for Verdaccio environment variables: public URL, forwarded protocol header, storage path and name, legacy token key and algorithm, Docker variables."
sources:
  - https://verdaccio.org/docs/env/
  - https://verdaccio.org/docs/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `VERDACCIO_PUBLIC_URL`: public base URL behind proxies; overrides Host and X-Forwarded-Proto and respects `url_prefix`.
- `VERDACCIO_FORWARDED_PROTO`: header that carries the protocol if not `X-Forwarded-Proto`, e.g.
  `VERDACCIO_FORWARDED_PROTO=CloudFront-Forwarded-Proto verdaccio --listen 5000`
- `VERDACCIO_STORAGE_PATH`: overrides the storage path from the config.
- `VERDACCIO_STORAGE_NAME`: database name for `@verdaccio/local-storage` (default `.verdaccio-db.json`).
- `VERDACCIO_LEGACY_ALGORITHM`: legacy token cipher, default `aes-256-ctr`.
- `VERDACCIO_LEGACY_ENCRYPTION_KEY`: 32-character key for legacy tokens (overrides the stored secret for that path only).
- `VERDACCIO_HANDLE_KILL_SIGNALS`: 6.x only, set `true` to enable graceful shutdown; removed in 7.x where it is always on.

Docker image variables: `VERDACCIO_APPDIR` (/opt/verdaccio), `VERDACCIO_USER_NAME` (verdaccio), `VERDACCIO_USER_UID` (10001), `VERDACCIO_PORT` (4873), `VERDACCIO_PROTOCOL` (http), `VERDACCIO_ADDRESS` (`[::]` on 7.x, `0.0.0.0` on 6.x).

Also: `NODE_ENV=production` flips the default log format to json; `DEBUG=verdaccio:middleware:log` shows hidden static and ping log lines; `XDG_CONFIG_HOME` and `XDG_DATA_HOME` choose default config and storage locations.

## Checked

2026-11-04. Confirmed against the Environment Variables, Command Line Tool and Logger pages (all variable names, defaults, 6.x/7.x notes, NODE_ENV log format, XDG locations, DEBUG namespace). Removed: the unsupported claim that `verdaccio --info` reports the process environment.
Method: documentation only; no commands were run.
