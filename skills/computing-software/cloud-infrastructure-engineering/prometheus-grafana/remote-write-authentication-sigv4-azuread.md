---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.remote-write-authentication-sigv4-azuread
name: remote-write-authentication-sigv4-azuread
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, remote-write, remote-write-sigv4, remote-write-azuread, amazon-managed-prometheus, azure-monitor-workspace, oauth2, basic-auth, irsa, workload-identity]
level: practitioner
status: docs-checked
description: "Authenticate Prometheus remote_write to Amazon Managed Prometheus (sigv4), Azure Monitor (azuread), and token/basic-auth backends, with workload identity."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write", "https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-onboard-ingest-metrics-new-Prometheus.html", "https://learn.microsoft.com/en-us/azure/azure-monitor/containers/prometheus-remote-write"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote write authentication

## Amazon Managed Service for Prometheus (sigv4)
```yaml
remote_write:
  - url: https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-xxxx/api/v1/remote_write
    sigv4:
      region: us-east-1
      # role_arn: arn:aws:iam::123456789012:role/amp-ingest   # optional assume-role
    queue_config: {max_samples_per_send: 1000, max_shards: 200, capacity: 2500}
```
- With `sigv4: {}` Prometheus uses the default AWS SDK credentials; the region falls back to that chain too. The AWS
  guide uses IAM roles for service accounts on EKS (service account annotated with `eks.amazonaws.com/role-arn`). IRSA-based
  SigV4 does not work off EKS/AWS with plain access keys. Prefer roles over `access_key`/`secret_key` in the file.
- The queue values above (`max_samples_per_send: 1000`, `max_shards: 200`, `capacity: 2500`) are the AWS guide's example.

## Azure Monitor workspace (azuread)
```yaml
remote_write:
  - url: https://<dce>.<region>.metrics.ingest.monitor.azure.com/dataCollectionRules/<dcr-id>/streams/Microsoft-PrometheusMetrics/api/v1/write?api-version=2023-04-24
    azuread:
      cloud: AzurePublic
      managed_identity: {client_id: <uami-client-id>}      # or oauth: {client_id, client_secret, tenant_id}
      # or workload_identity: {client_id, tenant_id}       # AKS workload identity
```
The identity needs **Monitoring Metrics Publisher** on the data collection rule; the assignment can take about 30 minutes, during which Prometheus may log HTTP 403. Version minimums from the Azure guide: Prometheus 2.45 for user-assigned managed identity, 2.48 for Microsoft Entra application auth, 3.5.0 for system-assigned managed identity, 3.7.0 for workload identity. The older sidecar approach is not supported after March 31, 2027.

## Bearer token / basic auth / OAuth2 (Grafana Cloud, Mimir, Thanos Receive)
```yaml
remote_write:
  - url: https://prometheus-prod-01.grafana.net/api/prom/push
    basic_auth: {username: "123456", password_file: /etc/secrets/gc-token}
  - url: https://mimir.internal/api/v1/push
    headers: {X-Scope-OrgID: team-a}                       # Mimir tenant
    authorization: {type: Bearer, credentials_file: /etc/secrets/token}
  - url: https://receive.internal/api/v1/receive
    oauth2: {client_id: prom, client_secret_file: /etc/secrets/cs, token_url: https://idp/oauth2/token, scopes: [metrics.write]}
```
Prefer the `*_file` variants (`password_file`, `credentials_file`, `client_secret_file`) so secrets stay out of the config file.

## Gotchas
- `sigv4` cannot be set together with `basic_auth`, `authorization`, `oauth2` or `azuread`; `azuread` likewise excludes `basic_auth`, `authorization`, `oauth2`, `sigv4` and `google_iam`.
- 4xx replies other than 429 are not retried (remote write 2.0 spec), so auth failures drop samples (`prometheus_remote_storage_samples_failed_total`) rather than queue them.
- Google Cloud does not support remote write; the `google_iam` block is reserved for future use.

## Checked
2026-10-28. Confirmed: Prometheus configuration page (`sigv4`, `azuread`, `basic_auth`, `authorization`, `oauth2`, exclusivity
rules, `*_file` fields, `google_iam` warning), Amazon Managed Service for Prometheus Helm guide (sigv4 config, queue values, IRSA note),
Azure Monitor remote write guide (URL pattern with `Microsoft-PrometheusMetrics`, `api-version=2023-04-24`, Monitoring Metrics Publisher,
version minimums, 403 delay, sidecar end of support), remote write 2.0 spec. Removed: `aps:RemoteWrite` action name, throttling and
quota claim, clock-skew figure, file re-read claim. Note: the AWS and Azure pages are product guides and change; re-check them for new releases.
Method: documentation only; no commands were run.

## Verify
- [ ] `promtool check config` passes.
- [ ] `prometheus_remote_storage_samples_failed_total` stays 0 and no 401/403 in logs.
- [ ] A query against the backend returns `up` for this Prometheus' external labels.
