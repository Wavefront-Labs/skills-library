---
id: computing-software.cloud-infrastructure-engineering.external-dns.node-source-records
name: node-source-records
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, node-source, no-exclude-unschedulable, expose-internal-ipv6, per-node-dns]
level: practitioner
status: docs-checked
description: "Publish one DNS record per cluster Node with --source=node: A and AAAA selection, cordoned nodes excluded by default, IPv6 flags and the docs example fqdn-template."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/nodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node source

`--source=node` synchronises a zone with the cluster's nodes.

- An `A` record per node `externalIP`; if none, any IPv4 `internalIP`.
- An `AAAA` record per node IPv6 `internalIP`. By default ExternalDNS exposes the IPv6 `ExternalIP`; `--expose-internal-ipv6` exposes internal IPv6 addresses explicitly.
- TTL comes from the `external-dns.kubernetes.io/ttl` node annotation.
- Unschedulable nodes are excluded: no records for Unhealthy, NotReady or SchedulingDisabled (cordoned) nodes, and existing ones are removed. `--no-exclude-unschedulable` always exposes nodes regardless of status, for example when you manage per-host records.

The docs example sets a name template:

```yaml
args:
- --source=node
- --provider=aws
- --zone-name-filter=external-dns-test.my-org.com
- --domain-filter=external-dns-test.my-org.com
- --aws-zone-type=public
- --registry=txt
- --fqdn-template={{.Name}}.external-dns-test.my-org.com
- --txt-owner-id=my-identifier
- --policy=sync
```

RBAC needs get/watch/list on `nodes` (the docs ClusterRole also lists services, pods, endpointslices, ingresses and routes).

## Checked

2026-11-04. Confirmed against the ExternalDNS Cluster Nodes as Source page (record types, TTL annotation, unschedulable handling, IPv6 behaviour, example spec, RBAC manifest). Removed an unsourced sync gotcha and a claim that a template is required.
Method: documentation only; no commands were run.
