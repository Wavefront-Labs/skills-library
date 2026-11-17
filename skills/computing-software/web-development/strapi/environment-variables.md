---
id: computing-software.web-development.strapi.environment-variables
name: environment-variables
category: computing-software
field: web-development
product: strapi
tags: [strapi, env, dotenv, secrets, jwt-secret, app-keys, node-env]
level: practitioner
status: docs-checked
description: "Strapi's own environment variables (APP_KEYS, JWT_SECRET, salts, DATABASE_*) and the env() helper with casting."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment variables

Defined in `.env` (path override: `ENV_PATH`, default `./.env`) and read in config with the `env()` helper, which can cast types (for example `env.int('PORT', 1337)`).

| Variable | Purpose | Default |
|---|---|---|
| `HOST` | listen address | `0.0.0.0` |
| `PORT` | listen port | `1337` |
| `APP_KEYS` | comma-separated keys signing cookies and secrets | auto-generated |
| `API_TOKEN_SALT` | salt for API tokens | auto-generated |
| `ADMIN_JWT_SECRET` | admin panel JWT secret; required when `admin.serveAdminPanel` is true | auto-generated |
| `JWT_SECRET` | JWT secret for Users & Permissions | auto-generated |
| `TRANSFER_TOKEN_SALT` | transfer tokens salt | auto-generated |
| `DATABASE_CLIENT` | database client | `sqlite` |
| `DATABASE_FILENAME` | SQLite file | `.tmp/data.db` |
| `NODE_ENV` | environment type; `production` enables specific behaviors | `'development'` |
| `STRAPI_TELEMETRY_DISABLED` | stop telemetry | `false` |
| `STRAPI_LICENSE` | license key for Enterprise Edition | - |
| `BROWSER` | open the admin panel at startup | `true` |

Prefix a name with `STRAPI_ADMIN_` to expose it to the admin front end (not on Strapi Cloud).

Per-environment config files live in `./config/env/{environment}/{filename}` and are merged over the base `./config` files, with the environment taken from `NODE_ENV` (default `development`); for example `NODE_ENV=production` loads `./config/*` plus `./config/env/production/*`, and the production values override the defaults.

## Checked

2026-11-04: checked against the Strapi docs page Environment variables configuration (configurations/environment). Confirmed: every variable listed in the table with its description and default, `ENV_PATH`, `STRAPI_ADMIN_` prefix and the Strapi Cloud exception, `./config/env/{environment}/{filename}` merge behaviour. Corrected: `NODE_ENV` default is `'development'`. Removed: `env.bool`, which this page does not mention (only the env() helper and `env.int` in an example).

Method: documentation only; no commands were run.
