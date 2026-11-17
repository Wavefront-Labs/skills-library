---
id: computing-software.cloud-infrastructure-engineering.external-dns.scaling-and-kube-api-limits
name: scaling-and-kube-api-limits
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, kube-api-qps, kube-api-burst, split-instances, kube-api-request-timeout, large-clusters]
level: advanced
status: docs-checked
description: "Scale ExternalDNS on big clusters: scope resources, split into instances with distinct owners, and tune --kube-api-qps, --kube-api-burst and request timeout."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling ExternalDNS

Three principles, applied together.

1. **Scope resources.** The fewer objects watched and zones managed, the lower the memory, API calls and reconcile time. Filter by service type, label, annotation, domain and zone ID.
2. **Split instances.** One instance across many zones or sources has a large reconcile surface. Run several, each owning a distinct zone set, namespace or source type. Each needs its own `--txt-owner-id` and non-overlapping `--domain-filter` or `--zone-id-filter`.
3. **Reduce reconcile pressure.** Tune the interval to your real change rate and use event-driven reconciliation for fast reaction. Raise `--kube-api-request-timeout` (default 30s per request) when the API server is slow.

**Kubernetes API rate limits.** ExternalDNS inherits client-go defaults of 5 QPS and 10 burst. Raise them for many sources or high reconcile frequency; lower them if you share quota with many controllers.

```sh
# high-throughput instance
--kube-api-qps=20
--kube-api-burst=40
# low-priority instance on a busy cluster
--kube-api-qps=2
--kube-api-burst=5
```

When throttled, the log contains `consider raising --kube-api-qps/--kube-api-burst`.

Provider batch size, record cache and zone cache flags live in the rate-limits page.

## Checked

2026-11-04. Confirmed against the ExternalDNS Operational Best Practices page (Scaling on Large Clusters): three principles, 30s request timeout default, client-go 5 QPS and 10 burst, the example values and the throttling log text. Nothing removed.
Method: documentation only; no commands were run.
