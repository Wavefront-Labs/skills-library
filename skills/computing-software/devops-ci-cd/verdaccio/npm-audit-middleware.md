---
id: computing-software.devops-ci-cd.verdaccio.npm-audit-middleware
name: npm-audit-middleware
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [audit, npm-audit, middleware, audit-middleware, vulnerability-scan]
level: practitioner
status: docs-checked
description: "Enable the built-in audit middleware so npm audit requests are handled by Verdaccio, and the optional timeout setting."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Verdaccio ships a built-in middleware plugin that handles `npm audit`. New installs have it enabled; older config files need the block added:

```yaml
middlewares:
  audit:
    enabled: true
    # timeout: 10000
```
Middleware plugins live under the `middlewares` namespace (see the plugins page, which uses audit as the base example).

Verify: `middlewares.audit.enabled` is true in the config the server loaded.

Related: package filtering hides risky versions before they are installed; audit reports problems in what is already installed.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Audit) and Plugins (Middleware Configuration). Confirmed: the built-in audit middleware, enabled by default on new installs, the middlewares.audit block with the optional timeout, and the plugins page using it as the example; package filter hiding versions. Removed or corrected: the verify command and the claim about audit lines in the server log.

Method: documentation only; no commands were run.
