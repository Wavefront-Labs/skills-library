---
id: computing-software.devops-ci-cd.verdaccio.default-config-walkthrough
name: default-config-walkthrough
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [default-config, config-yaml, packages-section, config-yaml-sections, defaults, uplinks]
level: intro
status: docs-checked
description: "Read the default Verdaccio config.yaml section by section: storage, auth, uplinks, packages, audit middleware and log, and what each default allows."
sources:
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The generated `config.yaml` is the cornerstone of a deployment.

```yaml
storage: ./storage
auth:
  htpasswd:
    file: ./htpasswd
uplinks:
  npmjs:
    url: https://registry.npmjs.org/
packages:
  '@*/*':
    access: $all
    publish: $authenticated
    unpublish: $authenticated
    proxy: npmjs
  '**':
    access: $all
    publish: $authenticated
    unpublish: $authenticated
    proxy: npmjs
middlewares:
  audit:
    enabled: true
log:
  type: stdout
  format: pretty
  level: http
```
Meaning: anyone may read; only logged-in users may publish or unpublish; anything not stored locally is fetched from npmjs and cached. Scoped packages are matched before the `**` catch-all.

Other top-level keys: `plugins` (plugin directory), `web`, `security`, `server`, `publish`, `url_prefix`, `user_agent`, `userRateLimit`, `max_body_size` (10mb default), `listen`, `https`, `notify`, `filters`, `flags`.

Gotcha: if the `packages` section is missing, nobody can access, publish or unpublish anything. The default htpasswd plugin lets anyone register, so restrict `max_users` or use another auth plugin before exposing it.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (default configuration and sections) and Package Access. Confirmed: the default config.yaml, its meaning, the other top-level keys, the 10mb body default, the missing packages section and the open htpasswd registration. Removed or corrected: nothing.

Method: documentation only; no commands were run.
