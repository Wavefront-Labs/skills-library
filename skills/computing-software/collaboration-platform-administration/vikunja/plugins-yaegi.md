---
id: computing-software.collaboration-platform-administration.vikunja.plugins-yaegi
name: plugins-yaegi
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, plugins-enabled, yaegi-loader, native-plugin-deprecated, plugin-routes]
level: advanced
status: docs-checked
description: "Enable and manage experimental Vikunja backend plugins with the Yaegi source loader: config, directory layout, routes, removal, trust and known limits."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugins are experimental and backend-only. They can add API endpoints, listen to events and run migrations. Plugins are off by default:

```yaml
plugins:
  enabled: true
  dir: "plugins"
  loader: yaegi
```

`dir` is relative to the binary or absolute. An invalid `loader` is a fatal startup error. Yaegi (recommended, from 2.3.0) interprets Go source: each plugin is a subdirectory with `.go` files, no compilation, works on Windows. The native loader (`.so` files) is deprecated, Linux/macOS only, and needs the exact same Go version as the binary.

Install: copy the plugin directory, restart, check logs for `Loaded plugin <name>`. Remove: stop Vikunja, delete the directory, restart. Plugins cannot be unloaded at runtime.

Routes: authenticated under `/api/v1/plugins/`, unauthenticated under `/plugins/` (rate-limited). 404 means initialization failed or no restart.

Security: plugins run with full Vikunja permissions and can reach the database and network. Read the source first, back up before plugins that migrate, keep files readable by the Vikunja user.

Limits: Yaegi evaluates files individually, so multi-file plugins may hit ordering problems.

## Checked

2026-11-04. Confirmed against the Vikunja Plugins page (setup/plugins): experimental and backend-only, capabilities, default-off config, loader validation, Yaegi from 2.3.0 and native loader limits, install and removal steps, log message, route prefixes, 404 cause, trust warnings and known limitations. Nothing removed.

Method: documentation only; no commands were run.
