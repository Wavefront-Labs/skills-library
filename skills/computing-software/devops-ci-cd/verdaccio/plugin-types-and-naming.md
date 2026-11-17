---
id: computing-software.devops-ci-cd.verdaccio.plugin-types-and-naming
name: plugin-types-and-naming
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [plugins, plugin-prefix, auth-plugin, plugin-types, plugin-order, middleware-plugin, storage-plugin, theme]
level: practitioner
status: docs-checked
description: "Verdaccio's five plugin types, the verdaccio-xxx naming rule and pluginPrefix, how to configure auth, middleware, store, theme and filters, and plugin order."
sources:
  - https://verdaccio.org/docs/plugins/
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Five types: authentication, middleware, storage, theme UI, filters. Install, then configure in `config.yaml`:

```
npm install --global verdaccio-activedirectory
```
```yaml
auth:
  activedirectory:
    url: 'ldap://10.0.100.1'
    baseDN: 'dc=sample,dc=local'
    domainSuffix: 'sample.local'
middlewares:
  audit:
    enabled: true
store:
  memory:
    limit: 1000
theme:
  dark: { option1: foo }
filters:
  plugin-secfilter:
    block:
      - scope: '@evil'
```
Rules:
- Plugins are named `verdaccio-<name>`; change the prefix with `server.pluginPrefix` (no dash, e.g. `acme` resolves `s3` to `acme-s3`). It applies to every category.
- Scoped plugin names work (`'@my-org/auth-awesome-plugin'`).
- Several auth plugins can be listed; order matters because credentials resolve in order. Comment out `htpasswd` to disable it.
- If `store` is set, `storage` is ignored.
- Only one theme loads at a time.
- 7.x loads plugins asynchronously with CommonJS and ESM interop, so pure ESM plugins work.
- `plugins: ./plugins` sets the plugin directory (useful in Docker/Kubernetes).

## Checked

2026-11-04. Read the Verdaccio documentation pages: Plugins and Configuration (Custom plugin prefix). Confirmed: the five plugin types, the verdaccio-xxx naming and server.pluginPrefix, scoped plugins, ordered auth plugins, store overriding storage, one theme, async loading in 7.x and the plugins directory. Removed or corrected: nothing.

Method: documentation only; no commands were run.
