---
id: computing-software.devops-ci-cd.argo-rollouts.prometheus-metric-provider
name: prometheus-metric-provider
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [prometheus, metric-provider, rangequery, sigv4, oauth2, basicauth, analysis, argo-rollouts]
level: practitioner
status: docs-checked
description: "Query Prometheus from an AnalysisTemplate, including range queries, headers, timeouts and managed-service authentication."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/analysis/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Prometheus provider runs a PromQL query and exposes the result as a vector, so conditions typically index `result[0]`.

```yaml
provider:
  prometheus:
    address: http://prometheus.example.com:9090
    timeout: 40          # seconds
    headers:
      - key: X-Scope-OrgID
        value: tenant_a
    query: |
      sum(irate(istio_requests_total{destination_service=~"{{args.service-name}}",response_code!~"5.*"}[5m])) /
      sum(irate(istio_requests_total{destination_service=~"{{args.service-name}}"}[5m]))
```

Validate the PromQL in the Prometheus UI first.

**Range queries** return many values, so assert on all of them. `result[0] < 1000` checks only the first; `all(result, # < 1000)` checks every value:

```yaml
provider:
  prometheus:
    rangeQuery:
      start: 'now() - duration("{{args.lookback-duration}}")'
      end: 'now()'
      step: 1m
```

**Authentication** options under `authentication`: `sigv4` (region, profile, roleArn) for Amazon Managed Prometheus, with IRSA attached to the analysis namespace; `google: {}` for Google Managed Prometheus; `oauth2` (tokenUrl, clientId, clientSecret, scopes), which fetches a token and sends `Authorization: Bearer`; and `basicAuth` (username, password) such as Grafana Cloud. Feed secrets from args with `secretKeyRef`.

`insecure: true` skips TLS verification. Resolved queries appear in the `Metadata` map of the MetricsResult.

Verify by checking the resolved query in the AnalysisRun's `Metadata` map.

## Checked

2026-11-08. Confirmed against the Argo Rollouts Prometheus page (read in full): vector results, timeout in seconds, headers, rangeQuery with all(), sigv4, google, oauth2, basicAuth, Metadata map, insecure option.

Removed or corrected: replaced the unsourced kubectl get analysisrun verify command.

Method: documentation only; no commands were run.
