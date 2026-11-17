---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.grafana-lgtm-datasource-provisioning
name: grafana-lgtm-datasource-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [datasource-provisioning, grafana, provisioning-yaml, loki-datasource, tempo-datasource, mimir-datasource, uid-linking]
level: practitioner
status: draft
description: "Provision Loki, Tempo and Mimir data sources in Grafana with stable UIDs so correlations work across them."
sources: ["https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: reproducible data sources with working cross-links.

File `/etc/grafana/provisioning/datasources/lgtm.yaml`:
```yaml
apiVersion: 1
datasources:
  - name: Mimir
    uid: mimir
    type: prometheus
    access: proxy
    url: http://mimir-nginx/prometheus
    jsonData:
      httpHeaderName1: X-Scope-OrgID
      prometheusType: Mimir
      exemplarTraceIdDestinations:
        - name: trace_id
          datasourceUid: tempo
    secureJsonData:
      httpHeaderValue1: team-a
  - name: Loki
    uid: loki
    type: loki
    access: proxy
    url: http://loki-gateway
    jsonData:
      maxLines: 1000
      derivedFields:
        - name: TraceID
          matcherRegex: 'trace_id=(\w+)'
          url: '$${__value.raw}'
          datasourceUid: tempo
  - name: Tempo
    uid: tempo
    type: tempo
    access: proxy
    url: http://tempo-query-frontend:3200
    jsonData:
      tracesToLogsV2:
        datasourceUid: loki
        filterByTraceID: true
      tracesToMetrics:
        datasourceUid: mimir
      serviceMap:
        datasourceUid: mimir
      nodeGraph:
        enabled: true
```
Gotchas
- UIDs referenced across sources must match exactly; renaming a data source name is safe, changing a UID breaks links.
- `$$` escapes `$` in provisioning files.
- Secrets belong in `secureJsonData` or env vars (`$__env{...}`), not `jsonData`.
- Provisioned data sources are read-only in the UI.

## Verify
Restart Grafana, open Connections > Data sources, press Save & test on each; the Tempo trace view shows "Logs for this span" links.
