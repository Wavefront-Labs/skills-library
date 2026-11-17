---
id: computing-software.systems-network-administration.coredns.coredns-kubernetes-basics
name: coredns-kubernetes-basics
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, kubernetes, service-discovery, cluster-dns, zones]
level: intro
status: docs-checked
description: "Serve Kubernetes cluster DNS with the kubernetes plugin, its default behaviour, in-cluster connection and reverse zones."
sources:
  - https://coredns.io/plugins/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace kube-dns with CoreDNS in a cluster.

The plugin implements the Kubernetes DNS-Based Service Discovery Specification. It can be used once per server block.

Syntax: `kubernetes [ZONES...]`. With no zones it uses the block's zone, handles all queries there and connects in-cluster with the service account. By default it does not provide PTR records for services or A records for pods. If ZONES is given it is authoritative for all of them.

Example handling cluster.local and reverse lookups for 10.0.0.0/17, verifying pods:

```
10.0.0.0/17 cluster.local {
    kubernetes {
        pods verified
    }
}
```

stubDomains and upstreamNameservers are implemented with the forward plugin in separate blocks:

```
cluster.local:53 { kubernetes cluster.local }
example.local { forward . 10.100.0.10:53 }
. { forward . 8.8.8.8:53 }
```

PTR records: one is created for every Pod selected by a Service; a Pod selected by several Services gets one per Service.

Endpoints are watched via the discovery.EndpointSlices API. Zone transfers are enabled through the transfer plugin.

## Checked

2026-11-08. Read the kubernetes plugin README (raw source of the cited page) in full. Claims about defaults, once-per-block, PTR and EndpointSlice watching, the verified-pods example and the stubDomains example match it.

Method: documentation only; no commands were run.
