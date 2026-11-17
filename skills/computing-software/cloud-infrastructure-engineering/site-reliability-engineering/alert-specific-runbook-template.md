---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.alert-specific-runbook-template
name: alert-specific-runbook-template
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, runbooks, alert-runbook-template, playbooks, alert-annotations, runbook-url]
level: practitioner
status: draft
description: "Write an alert-specific runbook from a standard template (meaning, impact, diagnosis, mitigation, escalation) and link it from every alert via runbook_url annotations."
sources: ["https://sre.google/sre-book/being-on-call/", "https://runbooks.prometheus-operator.dev/", "https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alert-specific runbook template

**Goal:** whoever is paged can act in minutes, even if they have never seen this alert.

## Link from the alert
```yaml
- alert: CheckoutHighErrorRate
  expr: job:checkout_errors:ratio_rate5m > 0.05
  for: 5m
  labels: { severity: page, team: payments }
  annotations:
    summary: "Checkout error rate {{ $value | humanizePercentage }}"
    description: "More than 5% of checkout requests failing for 5m in {{ $labels.cluster }}."
    runbook_url: "https://runbooks.example.com/payments/CheckoutHighErrorRate"
    dashboard_url: "https://grafana.example.com/d/checkout?var-cluster={{ $labels.cluster }}"
```
CI check: every alert rule with `severity: page` must have a `runbook_url` that resolves.

## Template
```markdown
# CheckoutHighErrorRate
## Meaning
What the alert measures and its threshold, in one or two sentences.
## Impact
Who is affected and how (users cannot pay). Related SLO: checkout availability 99.9%.
## Diagnosis
1. Open dashboard <link>. Is the error rate across all clusters or one?
2. Check recent deploys/flags: <annotation link / command>.
3. Check payment provider status and `payment_provider_errors_total` <query link>.
4. Logs: `{app="checkout"} |= "level=error"` in Loki <link>.
## Mitigation
- Recent deploy: roll back `kubectl argo rollouts undo checkout -n payments`.
- Single cluster: shift traffic `<command>`.
- Provider outage: enable fallback provider flag `payments.fallback=true`.
## Escalation
Payments on-call secondary -> payments engineering lead -> IC for SEV1. Provider support: <contact>.
## Notes / history
Past incidents: <postmortem links>. Last reviewed: 2026-10-01 by <name>.
```

## Practices
- One runbook per alert; keep diagnosis steps as links/queries, not prose.
- Review the runbook after each page that used it (was anything wrong or missing?).
- If the mitigation is fully mechanical, automate it and keep the runbook for verification.

## Verify
- [ ] All paging alerts have runbooks with "last reviewed" within 6 months; on-call feedback captured after use.
