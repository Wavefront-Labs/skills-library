---
id: computing-software.cloud-infrastructure-engineering.fluentd.service-discovery-srv
name: service-discovery-srv
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, service-discovery, srv, dns, out-forward]
level: practitioner
status: docs-checked
description: "Discover Fluentd forward targets from DNS SRV records with the srv service discovery plugin: service, proto, hostname, interval, dns_server_host."
sources:
  - https://docs.fluentd.org/service_discovery/srv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd srv service discovery
Updates `out_forward` targets from an RFC 2782 SRV record. Example: targets come from `_fluentd._tcp.example.com`:

```
<match pattern>
  @type forward
  <service_discovery>
    @type srv
    service fluentd
    proto tcp
    hostname example.com
  </service_discovery>
</match>
```
Parameters (all since 1.10.0):
- `service` (required): service name without the underscore.
- `proto`: default `tcp`, without the underscore.
- `hostname` (required): the name part of the record.
- `dns_server_host`: DNS server to ask (default nil).
- `interval`: interval of sending requests to the DNS server (integer), default 60.
- `dns_lookup`: default true; resolves the SRV target hostname to an IP.
- `shared_key`, `username`, `password`: per-server authentication (default nil).

The plugin uses the `timer` plugin helper.

## Checked

2026-11-04. Confirmed against the Fluentd srv service discovery page (docs.fluentd.org/service_discovery/srv): example config, parameters, defaults and 1.10.0 version, timer helper. Dropped the unit "seconds" for interval (the page gives none). The page also calls proto required while listing default tcp; this skill keeps the default.

Method: documentation only; no commands were run.
