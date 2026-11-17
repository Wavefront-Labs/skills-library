---
id: computing-software.cloud-infrastructure-engineering.external-dns.alerting-on-key-metrics
name: alerting-on-key-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, prometheus-alerts, consecutive-soft-errors, registry-errors-total, source-errors-total, verified-records]
level: practitioner
status: docs-checked
description: "Which ExternalDNS metrics to alert on: consecutive soft errors, source and registry errors, verified records, and watching restarts for hard-exit crashloops."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics worth alerting on

| Metric | Alert when |
|---|---|
| `external_dns_controller_consecutive_soft_errors` | greater than 0 for more than one reconcile cycle |
| `external_dns_source_errors_total` | sustained increase (Kubernetes API errors from informers) |
| `external_dns_registry_errors_total` | any increase (TXT or DynamoDB registry failures) |
| `external_dns_controller_verified_records` | unexpected drop (records no longer owned by this instance) |

**Hard exits are invisible to the soft-error metric.** A hard error that kills the process does not increment `consecutive_soft_errors`. Watch `kube_pod_container_status_restarts_total` and alert on `CrashLoopBackOff`.

**Invalid endpoints.** CNAME self-references, malformed MX/SRV records and unsupported alias types are dropped by the dedup layer with only a log warning. Surface them as events:

```sh
--events-emit=RecordError
kubectl get events --field-selector reason=RecordError
```

The metrics page also lists `external_dns_source_invalid_endpoints`, partitioned by `record_type` and `source_type`, which counts endpoints currently rejected for invalid configuration. The best-practices page describes that gauge as work in progress, so confirm it exists in your release.

Full metric list: the monitoring metrics page.

**Verify:** scrape the pod's metrics endpoint and confirm the four series above exist before writing alert rules.

## Checked

2026-11-04. Read the operational best practices page (Key metrics table, Kubernetes Events for invalid endpoints, crashloop amplification) and the metrics page. Confirmed the four alert rows, the hard-exit remark with kube_pod_container_status_restarts_total, the RecordError event command, and that source_invalid_endpoints appears in the metrics table while the best-practices page calls it work in progress. Removed nothing.

Method: documentation only; no commands were run.
