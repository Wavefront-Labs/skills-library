---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.discovery-dns
name: discovery-dns
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, service-discovery, dns, srv, a-record, discovery-type]
level: practitioner
status: docs-checked
description: "Use DNS service discovery in APISIX: discovery.dns servers and record order in config.yaml, discovery_type dns upstreams, and how A and SRV records set port and weight."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/discovery/dns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS service discovery

`conf/config.yaml`:

```yaml
discovery:
  dns:
    servers:
      - "127.0.0.1:8600"          # use the real address of your DNS server
    order:                        # record types tried when resolving
      - last                      # last previously successful type for a hostname
      - SRV
      - A
      - AAAA
      - CNAME
```

Upstream:

```json
{ "id": 1, "discovery_type": "dns", "service_name": "test.consul.service", "type": "roundrobin" }
```

Notes:
- A records: every returned IP is used with the same weight (1).
- SRV records set port and weight per target. Lower priority is chosen first (the stored value is negative); weight 0 counts as 1; port 0 falls back to the protocol default.
- Override the port by appending it to `service_name`, for example `"test.consul.service:1980"`, or with an SRV record.

## Checked

2026-11-04: read the DNS discovery page; the config block, default order SRV, A, AAAA, CNAME with `last` for cache refresh, the upstream example, same-weight A records, SRV priority sign, weight 0 as 1, port 0 fallback and the service_name port override match. Nothing removed.

Method: documentation only; no commands were run.
