---
id: computing-software.devops-ci-cd.argo-rollouts.datadog-metric-provider
name: datadog-metric-provider
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [datadog, metric-provider, api-v2, formula, queries, secret, analysis, argo-rollouts]
level: advanced
status: docs-checked
description: "Query Datadog from an AnalysisTemplate using API v1 or v2, with credentials from a Secret."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/analysis/datadog/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Datadog provider takes a query and interval. The provider's `apiVersion` (v1 or v2, default v1) refers to the Datadog API version, not the Kubernetes one.

```yaml
metrics:
  - name: error-rate
    interval: 5m
    successCondition: default(result, 0) < 0.01
    provider:
      datadog:
        apiVersion: v2
        interval: 5m
        query: |
          sum:requests.error.rate{service:{{args.service-name}}}
```

Credentials live in a Secret named `datadog` in the Argo Rollouts namespace:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog
type: Opaque
stringData:
  address: https://api.datadoghq.com
  api-key: <datadog-api-key>
  app-key: <datadog-app-key>
```

To use a Secret from the AnalysisTemplate's namespace instead, add `secretRef` (the Secret `name` and `namespaced: true`) under the datadog provider. Lookup order per the docs: the `secretRef` Secret in the template's namespace, then environment variables, then the Secret named `datadog` in the namespace where Argo Rollouts runs.

v2 notes: the `formula` and `queries` properties are only available as of v1.7. To migrate a simple v1 query with no formula, just change `apiVersion` to v2. If the v1 query used a formula (for example `moving_rollup(...)/...`), you must rewrite it using `queries` plus a `formula`.

Empty results from a quiet interval yield `nil`, so wrap `result` in `default(result, 0)` to avoid evaluation errors.

Verify with `kubectl describe analysisrun RUN` and compare to the Datadog UI.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/analysis/datadog/.

Removed or corrected: the claim to pick the address per Datadog site; the namespaced-secret description was corrected to the AnalysisTemplate namespace with its lookup order.

Method: documentation only; no commands were run.
