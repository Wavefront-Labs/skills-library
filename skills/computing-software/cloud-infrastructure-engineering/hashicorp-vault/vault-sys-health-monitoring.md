---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-sys-health-monitoring
name: vault-sys-health-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-monitoring, vault-telemetry, sys-health]
level: practitioner
status: docs-checked
description: "Read sys/health status codes, enable Prometheus telemetry and scrape sys/metrics, with the documented listener option for unauthenticated scrapes."
sources: ["https://developer.hashicorp.com/vault/api-docs/system/health", "https://developer.hashicorp.com/vault/api-docs/system/metrics", "https://developer.hashicorp.com/vault/docs/configuration/telemetry", "https://developer.hashicorp.com/vault/docs/configuration/listener/tcp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```hcl
telemetry {
  prometheus_retention_time = "60s"
  disable_hostname = true
}
```

```sh
curl -s 'https://vault.example.com:8200/v1/sys/metrics?format=prometheus' -H "X-Vault-Token: $T"
curl -s -o /dev/null -w '%{http_code}' https://vault.example.com:8200/v1/sys/health
```

`sys/health` status codes: `200` initialized, unsealed and active; `429` unsealed standby; `472` disaster recovery secondary; `473` performance standby; `501` not initialized; `503` sealed. A standby returning `429` is not a failure for a load-balancer probe, so use the query parameters `standbyok`, `perfstandbyok`, or override codes with `activecode`, `standbycode`, `drsecondarycode`, `performancestandbycode`, `sealedcode`, `uninitcode`. In rare cases such as cluster instability a node can return `429` although it is a DR secondary or performance standby.

Telemetry notes:
- `prometheus_retention_time` defaults to `24h`; setting it to `0` disables Prometheus telemetry.
- `disable_hostname` stops gauge values being prefixed with the hostname; the docs recommend it for Prometheus, optionally with `enable_hostname_label`.
- The `sys/metrics` output includes counters such as `vault_audit_log_request_failure`, which is worth alerting on because audit failures can make Vault unavailable when no audit device works.
- A listener can set `unauthenticated_metrics_access = true` to allow unauthenticated access to `/v1/sys/metrics`; otherwise send a token. Unauthenticated requests to `sys/metrics` are not audited when that is enabled.

## Checked
2026-11-03. Confirmed on the sys/health page (codes and parameters), the sys/metrics page (Prometheus format, `vault_audit_log_request_failure`), the telemetry page (`prometheus_retention_time`, `disable_hostname`), the TCP listener page (`unauthenticated_metrics_access`) and the audit page (unavailability, exempt endpoints). Removed: metric names `vault_core_unsealed` and `vault_core_leadership_lost`, the alert list (Raft latency, lease backlog, disk, certificate expiry), the `sys/metrics` policy claim, and the Verify and runbook advice.
Method: documentation only; no commands were run.
