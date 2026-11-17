---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.deploy-standalone-mode
name: deploy-standalone-mode
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, deployment-modes, standalone, apisix-yaml, config-provider, no-etcd]
level: practitioner
status: docs-checked
description: "Run APISIX without etcd in standalone mode: YAML, JSON or API-driven config_provider, the conf/apisix.yaml #END marker and the PUT /apisix/admin/configs endpoint."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/deployment-modes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standalone deployment mode

File-driven YAML:

```yaml
deployment:
  role: data_plane
  role_data_plane:
    config_provider: yaml
```

File-driven JSON: same, with `config_provider: json`.

API-driven:

```yaml
deployment:
  role: traditional
  role_traditional:
    config_provider: yaml
```

Behavior:
- YAML mode reads `conf/apisix.yaml` and checks for changes every second. The file must end with `#END` or it will not load.
- JSON mode reads `conf/apisix.json`, checks every second, and needs no `#END` marker.
- File-driven mode can run with the Admin API disabled.
- API-driven mode starts with an empty config and is meant for the APISIX Ingress Controller and ADC. Updates go through `PUT /apisix/admin/configs` on port 9180. Use it directly only if you understand its behavior.

## Checked

2026-11-04: read the Deployment Modes page (standalone sections); the YAML and JSON data_plane blocks, the traditional-role API-driven block, one-second file checks, the #END requirement for YAML and not for JSON, the empty start in API-driven mode and PUT /apisix/admin/configs on 9180 match. Nothing removed.

Method: documentation only; no commands were run.
