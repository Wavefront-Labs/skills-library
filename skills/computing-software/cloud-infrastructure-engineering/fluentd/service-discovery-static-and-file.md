---
id: computing-software.cloud-infrastructure-engineering.fluentd.service-discovery-static-and-file
name: service-discovery-static-and-file
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, service-discovery, static, file, out-forward, sd-yaml]
level: practitioner
status: docs-checked
description: "Define Fluentd forward targets with the service_discovery section using the static plugin or a YAML/JSON target list file; server parameters and weights."
sources:
  - https://docs.fluentd.org/configuration/service_discovery-section
  - https://docs.fluentd.org/service_discovery
  - https://docs.fluentd.org/service_discovery/static
  - https://docs.fluentd.org/service_discovery/file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd service discovery: static and file
`<service_discovery>` sits under a `<match>` and sets target nodes dynamically; the page examples use `forward`. `@type` is `static`, `file` or `srv`.

**static** (since 1.8.0): a list of `<server>` blocks like the forward `server` directive.
```
<service_discovery>
  @type static
  <server>
    host 127.0.0.1
  </server>
</service_discovery>
```
Server parameters: `host` (required), `port` (default 24224), `name`, `shared_key`, `username`, `password`, `standby` (default false), `weight` (default 60).

**file**: re-reads a local file to update targets. `path` default `/etc/fluent/sd.yaml`; format by extension (`yaml`, `yml`, `json`); `conf_encoding` default `utf-8`.
```
<service_discovery>
  @type file
  path "/etc/fluentd/sd.yaml"
</service_discovery>
```
Target list entries carry `host`, `port`, `weight`, `name`, `shared_key`, `username`, `password`, `standby`. In the file, `host` and `port` are required:
```
- 'host': 127.0.0.1
  'port': 24224
  'weight': 1
  'name': server1
```

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/service_discovery-section, https://docs.fluentd.org/service_discovery/static, https://docs.fluentd.org/service_discovery/file and confirmed: plugin types, static and file parameters and defaults, target list format. Removed or reworded: the claim that core support is out_forward (the page examples show forward).

Method: documentation only; no commands were run.
