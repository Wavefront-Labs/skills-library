---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanagerconfig-crd
name: alertmanagerconfig-crd
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-operator, alertmanagerconfig-crd, alertmanager, namespaced-routing, multi-team-alerting, secrets]
level: practitioner
status: docs-checked
description: "Let teams own their alert routing with AlertmanagerConfig: namespace matcher injection, receivers from Secrets, selectors on the Alertmanager CR, and the matcher strategy."
sources: ["https://prometheus-operator.dev/docs/developer/alerting/", "https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1alpha1.AlertmanagerConfig", "https://github.com/prometheus/alertmanager#amtool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AlertmanagerConfig CRD

```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: checkout-routing
  namespace: checkout
  labels: {alertmanagerConfig: team}        # must match the Alertmanager's selector
spec:
  route:
    receiver: checkout-slack
    groupBy: [alertname]
    groupWait: 30s
    repeatInterval: 4h
    matchers:
      - {name: severity, value: page, matchType: "="}
  receivers:
    - name: checkout-slack
      slackConfigs:
        - apiURL: {name: checkout-slack-webhook, key: url}     # Secret in the same namespace
          channel: "#checkout-alerts"
          sendResolved: true
```
Select such objects from the Alertmanager CR with `spec.alertmanagerConfigSelector` (label match, as in the Operator alerting guide) and, to choose which namespaces to look in, `spec.alertmanagerConfigNamespaceSelector`.

## How it merges
- `spec.route` is added to the generated Alertmanager configuration as a first-level route. For that first-level route the operator removes any existing equality and regexp matcher on the `namespace` label and adds `namespace: <object namespace>`, unless the strategy says otherwise. The operator also forces `continue` to true on it.
- By default the config only applies to alerts whose `namespace` label equals the AlertmanagerConfig's namespace; inhibit rules from the object also apply only to those alerts.
- `spec.alertmanagerConfigMatcherStrategy.type` on the Alertmanager CR: default `OnNamespace`; `None` makes the routes and inhibit rules process all incoming alerts; `OnNamespaceExceptForAlertmanagerNamespace` exempts objects in the Alertmanager's own namespace.
- Secret references (`apiURL`, `routingKey` and so on) are Secret key selectors; the Secret must be in the same namespace as the AlertmanagerConfig object and accessible by the Prometheus Operator.
- A global AlertmanagerConfig can be named in the Alertmanager's `spec.alertmanagerConfiguration.name` (same namespace as the Alertmanager); for it the operator does not enforce a namespace label on routes and inhibition rules.
- Matchers take `name`, `value` and `matchType` (`=`, `!=`, `=~`, `!~`); `regex` is deprecated in favour of `matchType`.

## Debug
Test routing against the generated Alertmanager config with `amtool config routes test --config.file=<file> --tree --verify.receivers=<receiver> label=value ...` (Alertmanager README; `--verify.receivers` makes amtool exit 1 on mismatch).

## Verify
- [ ] The generated configuration contains the team route as a first-level route with a `namespace` matcher for the team's namespace.
- [ ] `amtool config routes test` returns the team receiver for a sample alert carrying that namespace label.

## Checked
Date: 2026-11-07. The Operator "Alerting Routes" guide was read in full (selectors, global alertmanagerConfiguration, Secret requirements). The AlertmanagerConfig API reference is about 650 KB and was searched, not read end to end: I read the Route, AlertmanagerConfigSpec, AlertmanagerConfigMatcherStrategy(Type), AlertmanagerConfiguration, Matcher, SlackConfig and PagerDutyConfig field entries. The amtool routes test command comes from the Alertmanager README (amtool Routes section). Removed as unconfirmed: the receiver-name prefix format (`checkout/checkout-routing/...`), the `alertmanager-main-generated` Secret and its gzip key, the "operator logs show rejected configs" claim and the nested pagerduty child route. Corrected: the draft only said `None` disables injection; the reference also lists `OnNamespaceExceptForAlertmanagerNamespace`.
Method: documentation only; no commands were run.
