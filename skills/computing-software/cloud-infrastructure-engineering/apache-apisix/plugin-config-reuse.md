---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.plugin-config-reuse
name: plugin-config-reuse
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, plugin-config, plugin-configs, reuse, route, admin-api]
level: practitioner
status: docs-checked
description: "Reuse plugin settings across APISIX routes with plugin_configs and plugin_config_id, how route plugins merge with them, and the 503 for a missing config."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/terminology/plugin-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin Config reuse

Create a shared set of plugins:

```shell
curl http://127.0.0.1:9180/apisix/admin/plugin_configs/1 \
-H "X-API-KEY: $admin_key" -X PUT -i -d '
{
    "desc": "blah",
    "plugins": {
        "limit-count": { "count": 2, "time_window": 60, "rejected_code": 503 }
    }
}'
```

Bind it to a route with `plugin_config_id`:

```shell
curl http://127.0.0.1:9180/apisix/admin/routes/1 \
-H "X-API-KEY: $admin_key" -X PUT -i -d '
{
    "uris": ["/index.html"],
    "plugin_config_id": 1,
    "upstream": { "type": "roundrobin", "nodes": { "127.0.0.1:1980": 1 } }
}'
```

Rules:
- The route's own `plugins` merge with the Plugin Config's plugins.
- If the same plugin is in both, the route's settings take priority.
- If the referenced Plugin Config ID does not exist, requests to the route return 503.

## Checked

2026-11-04: read the Plugin Config page; both curl examples, the 503 for a missing Plugin Config, and the merge rule (route plugin settings are not overridden by the Plugin Config) match. Nothing removed.

Method: documentation only; no commands were run.
