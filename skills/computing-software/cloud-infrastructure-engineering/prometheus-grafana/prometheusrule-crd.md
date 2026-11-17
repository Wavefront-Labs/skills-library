---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheusrule-crd
name: prometheusrule-crd
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-operator, prometheusrule-crd, rule-selectors, alerting-rules, recording-rules, admission-webhook, promtool]
level: practitioner
status: gated
description: "Ship rules as PrometheusRule objects: CR shape, ruleSelector/ruleNamespaceSelector matching, admission validation, testing with promtool, and debugging rules that never load."
sources: ["https://prometheus-operator.dev/docs/developer/alerting/", "https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.PrometheusRule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PrometheusRule CRD

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: checkout-slo
  namespace: checkout
  labels: {role: alert-rules}            # must match Prometheus spec.ruleSelector
spec:
  groups:
    - name: checkout.rules
      interval: 30s
      rules:
        - record: job:http_requests:rate5m
          expr: sum by (job, code) (rate(http_requests_total{job="checkout"}[5m]))
        - alert: CheckoutHighErrorRate
          expr: sum(job:http_requests:rate5m{code=~"5.."}) / sum(job:http_requests:rate5m) > 0.05
          for: 10m
          labels: {severity: page, team: checkout}
          annotations:
            summary: "Checkout 5xx above 5%"
            runbook_url: https://runbooks.example.com/checkout-errors
```

## Selection
The operator merges every PrometheusRule matching `spec.ruleSelector` in namespaces matching
`spec.ruleNamespaceSelector` into ConfigMaps `prometheus-<name>-rulefiles-N`, mounted and reloaded by the
config-reloader sidecar. Namespace-scoped rules can be forced to only see their namespace with
`spec.enforcedNamespaceLabel: namespace` (the operator injects `namespace="<ns>"` matchers). (gated: unconfirmed, source is paywalled or blocked) The field names `ruleSelector`, `ruleNamespaceSelector` and `enforcedNamespaceLabel` are confirmed in the operator API reference; the ConfigMap naming, sidecar reload and matcher injection need a Kubernetes cluster, which is not available here.

## Validation and tests
- The operator's admission webhook (if deployed) rejects invalid PromQL at `kubectl apply`. (gated: unconfirmed, source is paywalled or blocked) Needs a cluster with the webhook deployed; not run here.
- In CI, extract and test with promtool:
```bash
yq '.spec' prometheusrule.yaml > /tmp/rules.yml && promtool check rules /tmp/rules.yml
promtool test rules tests/checkout_test.yml        # rule_files: [/tmp/rules.yml]
```
The `.spec` of the example PrometheusRule above passed `promtool check rules` on 3.15.1 (extracted with PyYAML here instead of `yq`, which was not run).

## Debugging rules that don't appear
(gated: unconfirmed, source is paywalled or blocked) The kubectl steps below need a cluster and were not run here.
1. Labels match `ruleSelector`? `kubectl get prometheus -o jsonpath='{.spec.ruleSelector}'`.
2. Namespace matches `ruleNamespaceSelector`?
3. `kubectl -n monitoring get cm -l prometheus-name=k8s` - is the rule in the generated ConfigMap?
4. Operator logs: `invalid rule` errors exclude the whole PrometheusRule object.
5. Prometheus `/rules` page and `prometheus_rule_group_rules` metric.

## Verify
- [ ] Rule visible on `/rules` with health `ok`.
- [ ] `promtool test rules` runs in CI for every PrometheusRule.
