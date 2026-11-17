---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-dns-prepared-queries
name: consul-dns-prepared-queries
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, prepared-queries, query-failover, dns-templates]
level: practitioner
status: docs-checked
description: "Define Consul prepared queries with tag filtering and cross-datacenter failover, and use name-prefix templates for many services."
sources: ["https://developer.hashicorp.com/consul/docs/services/discovery/dns-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prepared queries are stored query definitions that DNS or the HTTP API can execute. They add behaviour static lookups lack: filter by several tags, restrict by node metadata, and fail over to other datacenters when no healthy local instance exists.

```sh
curl -s --request POST --data '{
  "Name": "web-prod",
  "Service": {
    "Service": "web",
    "Tags": ["prod"],
    "Failover": {"NearestN": 2}
  }
}' localhost:8500/v1/query
dig @127.0.0.1 -p 8600 web-prod.query.consul
```

A template (`"Template": {"Type": "name_prefix_match"}`) lets one definition serve many names.

Gotchas: creating a query needs `query:write`. `NearestN` forwards the query to up to N other datacenters ordered by median round trip time using network coordinates from the WAN gossip pool; `Targets` lists remote datacenters or cluster peers explicitly and cannot be combined with `NearestN`. A template applies to any lookup whose name starts with the template `Name`, resolved by longest prefix match; static queries are always resolved first, so they can override templates.

Verify: `dig @127.0.0.1 -p 8600 web-prod.query.consul` returns the healthy instances. The DNS form of a prepared query is `<query>.query`.

## Checked

2026-11-03. Confirmed against the Prepared Query HTTP API page (Template name_prefix_match and prefix resolution, Failover NearestN and Targets, query:write ACL) and the Consul DNS reference (`<query>.query` syntax). Removed: the execution-token claim, the WAN health claim, the query-name namespace claim, the maintenance-mode drill and the version-control advice, none of which a page states.

Method: documentation only; no commands were run.
