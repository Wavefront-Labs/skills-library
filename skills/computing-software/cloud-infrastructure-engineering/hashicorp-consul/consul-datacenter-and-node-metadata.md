---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-datacenter-and-node-metadata
name: consul-datacenter-and-node-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, node-meta, node-metadata, catalog-filter]
level: practitioner
status: docs-checked
description: "Add node_meta and service meta to Consul agents and use them for filtering catalog queries and prepared queries."
sources: ["https://developer.hashicorp.com/consul/docs/services/configuration/services-configuration-reference", "https://developer.hashicorp.com/consul/docs/services/discovery/dns-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metadata makes queries and automation precise without relying on naming conventions.

```hcl
node_meta {
  zone = "eu-west-1a"
  rack = "r12"
}
```

```sh
consul catalog nodes -node-meta=zone=eu-west-1a
curl -sG localhost:8500/v1/catalog/service/web --data-urlencode 'filter=NodeMeta.zone == "eu-west-1a"'
curl -sG localhost:8500/v1/health/service/web --data-urlencode 'filter=Service.Meta.owner == "payments"'
```

Gotchas: service `meta` allows up to 64 pairs; keys and values are strings, keys use only ASCII letters, digits, `_` and `-` and are limited to 128 characters, and values to 512 characters. The `node-meta` query parameter on the catalog endpoints is deprecated in favour of `filter` with the `NodeMeta` selector. Filtering is executed on the Consul server before data is returned.

Verify: filtered queries return only matching nodes and services.

## Checked

2026-11-03. Confirmed against the service definition reference (meta limits: 64 pairs, key characters, 128 and 512 character limits), the catalog HTTP API page (NodeMeta selector, node-meta deprecated), the filtering page, the consul catalog nodes page (-node-meta flag) and the health API page (Service.Meta selectors). Removed: the restart-for-node-meta claim, the secrets-visibility claim, the empty-list claim and the schema and quarterly review advice, none of which a page states.

Method: documentation only; no commands were run.
