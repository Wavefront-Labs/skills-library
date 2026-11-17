---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.discovery-nacos
name: discovery-nacos
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, service-discovery, nacos, discovery-args, namespace]
level: practitioner
status: docs-checked
description: "Discover upstream nodes from Nacos in APISIX: discovery.nacos defaults (prefix, fetch_interval, weight, timeouts) and namespace_id and group_name via discovery_args."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/discovery/nacos.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nacos service discovery

`conf/config.yaml` with defaults:

```yaml
discovery:
  nacos:
    host:
      - "https://${{NACOS_USERNAME}}:${{NACOS_PASSWORD}}@${{NACOS_HOST}}:${{NACOS_PORT}}"
    prefix: "/nacos/v1/"
    fetch_interval: 30    # seconds
    weight: 100           # default weight for nodes without one
    timeout:
      connect: 2000       # ms
      send: 2000
      read: 5000
```

Keep credentials in environment variables rather than literal values.

Route:

```json
{ "uri": "/nacos/*",
  "upstream": { "service_name": "APISIX-NACOS", "type": "roundrobin", "discovery_type": "nacos" } }
```

Namespace and group default to `public` and `DEFAULT_GROUP`; override with `discovery_args`:

```json
"discovery_args": { "namespace_id": "test_ns", "group_name": "test_group" }
```

## Checked

2026-11-04. Confirmed against the APISIX Nacos discovery page: prefix, fetch_interval, weight and the three timeout defaults, discovery_args with namespace_id and group_name and their defaults. Nothing removed.

Method: documentation only; no commands were run.
