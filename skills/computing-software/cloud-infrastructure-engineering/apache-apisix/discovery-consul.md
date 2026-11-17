---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.discovery-consul
name: discovery-consul
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, service-discovery, consul, discovery-type, fetch-interval]
level: practitioner
status: docs-checked
description: "Discover upstream nodes from Consul in APISIX: the discovery.consul block (servers, timeouts, weight, fetch_interval, sort_type) and a discovery_type consul route."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/discovery/consul.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consul service discovery

`conf/config.yaml`:

```yaml
discovery:
  consul:
    servers:
      - "http://127.0.0.1:8500"
    ssl_verify: true
    timeout:
      connect: 2000
      read: 2000
      wait: 60
    weight: 1
    fetch_interval: 3
    keepalive: true
    sort_type: "origin"
```

Route using it:

```shell
curl http://127.0.0.1:9180/apisix/admin/routes/1 -H "X-API-KEY: $admin_key" -X PUT -d '
{
  "uri": "/*",
  "upstream": {
    "service_name": "service_a",
    "type": "roundrobin",
    "discovery_type": "consul"
  }
}'
```

`service_name` is the name registered in Consul; `discovery_type` selects the registry.

The values above are the documented defaults (connect and read 2000 ms, wait 60 s, weight 1, `fetch_interval` 3 s, `keepalive` true, `sort_type` origin, `ssl_verify` true). `fetch_interval` only takes effect with `keepalive: false` (short polling); `keepalive: true` uses long polling and is recommended. `sort_type` takes `origin`, `host_sort`, `port_sort` or `combine_sort`.

## Checked

2026-11-04: read the Consul discovery page; the config block values equal the documented defaults, the route example matches, and `fetch_interval` scope and `sort_type` values were added from the page. Nothing removed.

Method: documentation only; no commands were run.
