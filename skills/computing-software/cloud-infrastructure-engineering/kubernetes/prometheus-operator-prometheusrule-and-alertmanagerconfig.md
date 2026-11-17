---
id: computing-software.cloud-infrastructure-engineering.kubernetes.prometheus-operator-prometheusrule-and-alertmanagerconfig
name: prometheus-operator-prometheusrule-and-alertmanagerconfig
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, prometheus-operator, prometheusrule, alertmanagerconfig, alertmanager, crd, rule-selector, promql, kube-prometheus-stack, routing, silences]
level: advanced
status: docs-checked
description: "Authoring PrometheusRule and AlertmanagerConfig CRDs under the Prometheus Operator, and why a syntactically valid rule or route silently never fires."
sources: ["https://prometheus-operator.dev/docs/api-reference/api/", "https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/platform/webhook/", "https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PrometheusRule and AlertmanagerConfig: valid YAML that still never fires

**Goal:** author alerting and routing as CRDs the way the Operator expects, and know the
three places a correct-looking rule or route silently does nothing — `ruleSelector` mismatch,
AlertmanagerConfig namespace scoping, and matcher precedence.

## 1. PrometheusRule mechanics
Like ServiceMonitor, `PrometheusRule` objects are **compiled by the Operator into a rule
file** mounted into Prometheus; they are not evaluated directly. Same selector chain applies:
`Prometheus.spec.ruleSelector` / `ruleNamespaceSelector` must match the PrometheusRule's
labels and namespace, or it is invisible — identical failure mode to ServiceMonitor
(see `computing-software.cloud-infrastructure-engineering.kubernetes.prometheus-operator-servicemonitor-and-podmonitor`).
Check what actually loaded:
```bash
curl -s localhost:9090/api/v1/rules
kubectl -n <prom-ns> logs sts/prometheus-<name> -c prometheus
```
The Operator's admission webhook (`/admission-prometheusrules/validate`) rejects semantically
invalid `PrometheusRule` objects at apply time, but it is optional: if you have not deployed and
registered it, `kubectl apply` only checks the CRD schema, not PromQL. Check the Prometheus logs
after any PrometheusRule change.

## 2. Alert state and labels that drive routing
Active alert elements are `pending` for the rule's `for:` duration before `firing` — a transient spike shorter than `for:` never alerts,
by design (debounce). `labels:` on the rule become the Alertmanager routing key;
`annotations:` carry display text such as summary and description; routes match on alert labels, so
put anything you route on in `labels:`.

For SLO-style burn-rate alerts specifically, see
`computing-software.cloud-infrastructure-engineering.kubernetes.slo-dashboards-for-kubernetes-workloads`
and `computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets`
for the multi-window multi-burn-rate pattern this CRD hosts.

## 3. AlertmanagerConfig: the scoping trap
`AlertmanagerConfig` is a **namespaced** CRD — the Operator merges every selected
`AlertmanagerConfig` object's `route`/`receivers` into the Alertmanager configuration (the base
config comes from the Secret named by `Alertmanager.spec.configSecret`, default
`alertmanager-<name>`, key `alertmanager.yaml`). Consequences:
- `Alertmanager.spec.alertmanagerConfigSelector` / `...NamespaceSelector` gates which configs
  are even considered — same pattern as Prometheus's rule/service selectors; a nil
  `alertmanagerConfigNamespaceSelector` means only the Alertmanager's own namespace is checked.
- With the default `alertmanagerConfigMatcherStrategy` (`OnNamespace`), an AlertmanagerConfig's route and
  inhibition rules only process alerts whose `namespace` label equals the object's namespace
  (`OnNamespaceExceptForAlertmanagerNamespace` lets configs in the Alertmanager's own namespace process
  all alerts). Teams expecting a totally independent routing tree are surprised by this.
- Receiver secrets (Slack webhook URLs, PagerDuty keys) referenced from an AlertmanagerConfig live in the
  **same namespace as the AlertmanagerConfig**, not the Alertmanager's namespace.

## 4. Matcher precedence and the "it matched the wrong receiver" bug
Alertmanager routing evaluates routes **depth-first, in order**, and stops at the first
matching leaf unless `continue: true` is set — a broad early matcher (e.g. `severity=~".*"`)
silently swallows every alert below it in the tree, sending everything to one receiver and
making more specific child routes dead code. When a new team's routing rule "doesn't work,"
check sibling and ancestor routes for an overly broad matcher before assuming the new rule's
matcher syntax is wrong.

## Gotchas
- `inhibit_rules` and silences operate independently of routing — a correctly routed alert
  can still never page because an inhibition rule (e.g. suppress `warning` when a `critical`
  with the same `alertname`+`cluster` is firing) matches unexpectedly broadly.
- Check Alertmanager's own logs after template changes, not just that a notification arrived.
- If the config Secret or its `alertmanager.yaml` key is missing, the Operator provisions a minimal
  configuration with one empty receiver, which effectively drops notifications.

## Verify
- [ ] `curl localhost:9090/api/v1/rules` shows every expected rule group with `health: ok`, none dropped from a sibling syntax error.
- [ ] The Alertmanager configuration the Operator generated (the Secret named after the Alertmanager) contains each team's route and receivers as intended.
- [ ] A deliberately tripped test rule reaches the intended receiver end to end.
- [ ] Inhibition rules are reviewed whenever a new severity label value is introduced.

## Checked

Checked against `prometheus-operator/prometheus-operator` main (latest release v0.94.2, 2026-10-23): `Documentation/api-reference/api.md` and `platform/webhook.md`.
Confirmed: `ruleSelector` and `ruleNamespaceSelector` fields, `alertmanagerConfigSelector`, `alertmanagerConfigNamespaceSelector` (nil means own namespace), `alertmanagerConfigMatcherStrategy` default `OnNamespace`, `configSecret` default `alertmanager-<name>` with key `alertmanager.yaml`, the PrometheusRule and AlertmanagerConfig validating webhook.
Removed as wrong or unconfirmed: the "operator v0.22" claim, the claim that CRD config replaces the hand-written config, the Prometheus group-rejection and template-error behaviours (the docs do not describe them).
Also checked: Prometheus `alerting_rules.md` (`for` and the pending state) and `querying/api.md` (`/api/v1/rules`, `/api/v1/targets`, `/api/v1/status/config`), and Alertmanager `docs/configuration.md` (routes traverse children in order, `continue` defaults to false, `inhibit_rules`).

Method: documentation only; no commands were run.
