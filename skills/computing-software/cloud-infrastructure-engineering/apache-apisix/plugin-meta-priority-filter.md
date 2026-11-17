---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.plugin-meta-priority-filter
name: plugin-meta-priority-filter
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, plugin-order, meta, priority, filter, disable, plugins-reload]
level: advanced
status: docs-checked
description: "Control APISIX plugin execution with _meta (priority, disable, filter, error_response), phase ordering, and enabling plugins in config.yaml with a hot reload."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/terminology/plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin _meta and ordering

Phase order: global-rule `rewrite`, local `rewrite`, global-rule `access`, local `access`. Within each group a higher priority number runs first; priority never moves a plugin across phases or between global and local groups.

`_meta` fields on a plugin instance:
- `priority`: overrides the default for that instance only. To run `limit-count` (default 1002) before `ip-restriction` (3000), set it above 3000. Remove the field to restore the default.
- `disable`: `true` skips the plugin.
- `filter`: array of `[var, operator, val]` evaluated per request, for example `[["arg_version", "==", "v2"]]`.
- `error_response`: fixed custom error body, for example `{"message": "Missing credential in request"}` for `jwt-auth`.

```json
{ "plugins": { "limit-count": { "_meta": { "priority": 3010 } } } }
```

Installed plugins are listed under `plugins` in `config.yaml`; comment one out (for example `# - mocking`) to prevent installation, then reload. For a runtime reload send `PUT /apisix/admin/plugins/reload` with `X-API-KEY`.

## Checked

2026-11-04: read the Plugin terminology page; execution order, the priority example (limit-count 1002, ip-restriction 3000, 3010), the _meta fields disable, filter, error_response and priority, the installation and reload text, and PUT /apisix/admin/plugins/reload match. Nothing removed.

Method: documentation only; no commands were run.
