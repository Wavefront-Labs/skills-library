---
id: computing-software.devops-ci-cd.backstage.config-app-config-files
name: config-app-config-files
category: computing-software
field: devops-ci-cd
product: backstage
tags: [app-config, backstage-env, config-loading, backstage]
level: intro
status: docs-checked
description: "Know how Backstage loads app-config.yaml, local overrides, BACKSTAGE_ENV files and environment variables."
sources:
  - https://backstage.io/docs/conf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backstage stores configuration in YAML. The defaults are `app-config.yaml` and `app-config.local.yaml` for local overrides. `BACKSTAGE_ENV` adds environment-based files and accepts one value or a comma-separated list. For `BACKSTAGE_ENV=e2e-test,production` the load order is:

1. `app-config.yaml`
2. `app-config.e2e-test.yaml`
3. `app-config.production.yaml`
4. `app-config.local.yaml`
5. `app-config.e2e-test.local.yaml`
6. `app-config.production.local.yaml`

All non-local environment files load before local ones, so local overrides always win; within each group the order is as specified. The base `app-config.yaml` is required by default, while the others are loaded only if they exist. Pass `--config <path>` flags to load other files; when any flag is given the default app-config files are NOT loaded unless you list them, and the last flag has the highest priority.

```yaml
app:
  title: Backstage Example App
  baseUrl: http://localhost:3000
backend:
  listen: 0.0.0.0:7007
  baseUrl: http://localhost:7007
organization:
  name: CNCF
```

Configuration can also be supplied with environment variables of the form `APP_CONFIG_<path>`, for example `APP_CONFIG_app_baseUrl=https://staging.example.com`. They have the highest priority, the value is parsed as JSON and falls back to a string, and the docs recommend using them sparingly, for example to reuse deployment artifacts across staging and production.

Frontend and backend share the same files, but only keys marked with frontend visibility reach the browser.

## Checked

2026-11-03. Confirmed against the Backstage Configuration and Writing Configuration pages: default files, `BACKSTAGE_ENV` ordering, `--config` behaviour, `APP_CONFIG_` overrides and priority, the sample config. Nothing removed.

Method: documentation only; no commands were run.
