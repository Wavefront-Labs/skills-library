---
id: computing-software.cloud-infrastructure-engineering.kubernetes.alert-hygiene-and-runbook-links
name: alert-hygiene-and-runbook-links
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, slo-dashboards, runbook-url, alerting, prometheusrule, alertmanager]
level: practitioner
status: docs-checked
description: "Keep Kubernetes alerts actionable: runbook_url on every alert, severity and ownership labels, sensible for durations, grouping and inhibition in Alertmanager."
sources: ["https://runbooks.prometheus-operator.dev/", "https://prometheus.io/docs/practices/alerting/", "https://prometheus.io/docs/alerting/latest/configuration/", "https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alert hygiene and runbook links

## Every alert carries
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata: {name: shop-alerts, namespace: shop, labels: {release: kube-prometheus-stack}}
spec:
  groups:
  - name: shop.rules
    rules:
    - alert: CheckoutHighErrorRate
      expr: job:checkout_errors:ratio_rate5m > 0.05
      for: 10m
      labels: {severity: critical, team: payments}
      annotations:
        summary: "Checkout error rate {{ $value | humanizePercentage }}"
        description: "More than 5 % of checkout requests failed for 10 minutes."
        runbook_url: "https://runbooks.example.com/payments/checkout-high-error-rate"
        dashboard_url: "https://grafana.example.com/d/checkout"
```
kube-prometheus-stack's default rules take their runbook links from `defaultRules.runbookUrl`
(`https://runbooks.prometheus-operator.dev/runbooks` in the chart's values); keep those and add local notes
where your setup differs.

## Runbook content
What it means, user impact, first three checks (commands), common causes and fixes, escalation.
A runbook link that 404s is worse than none; check links in CI.

## Alertmanager templates show it
```yaml
receivers:
- name: payments-slack
  slack_configs:
  - channel: '#payments-alerts'
    title: '{{ .CommonLabels.alertname }} ({{ .CommonLabels.severity }})'
    text: '{{ range .Alerts }}{{ .Annotations.summary }} <{{ .Annotations.runbook_url }}|runbook>{{ end }}'
```

## Hygiene rules
- Page only on symptoms (SLO burn, total outage); cause-level alerts go to tickets.
- `for:` long enough to skip blips, short enough to act before users notice.
- Route by `team` label; group by `alertname, namespace` to avoid storms.
- Inhibit (`inhibit_rules`): a critical alert suppresses warnings with the same labels, for example a
  node-level critical suppressing pod-level warnings on that node.
- Review monthly: delete alerts nobody acted on.

## Verify
`amtool check-config alertmanager.yaml` passes; a test alert reaches the right channel with a
working runbook link.

## Checked
2026-10-28. Confirmed: `amtool check-config`, `slack_configs` with `title`/`text`, `group_by` and
`inhibit_rules` against the Alertmanager configuration page; page on symptoms and the alert practices
against the Prometheus alerting-practices page; `humanizePercentage` in annotation templates against
kubernetes-mixin alert annotations; `defaultRules.runbookUrl` against the chart `values.yaml`. Removed: the
"5-15 minutes" figure and the claim that the mixin alerts link to the runbooks site by themselves.
The example URLs use `example.com` placeholders.
Method: documentation only; no commands were run.
