---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-failing-closed-considerations
name: opa-gatekeeper-failing-closed-considerations
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, failure-policy, fail-closed, availability, deadlock, failure-domains, ha]
level: sme
status: docs-checked
description: "Decide whether to set Gatekeeper failurePolicy to Fail, covering admission deadlock, control-plane availability, scoping the webhook and failure domains."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/failing-closed.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper failing closed considerations

Gatekeeper defaults to `failurePolicy: Ignore`; audit is expected to catch what slips through when the webhook is down. To fail closed, set the `failurePolicy` field of Gatekeeper's `ValidatingWebhookConfiguration` to `Fail` (manifest install; the doc's example sets it on both webhooks, `validation.gatekeeper.sh` and `check-ignore-label.gatekeeper.sh`; Helm or operator installs follow their own docs).

Considerations:
- Admission deadlock: delete every Node and Gatekeeper pods die; the webhook fails; adding a Node needs admission; it cannot succeed. Break it by deleting the webhook configuration (emergency procedure). Kubernetes does not subject edits to webhook configurations to admission. An external operator that enforces the webhook resource can interfere, so plan for that.
- Control-plane availability: the webhook sees all API requests by default, so API availability becomes bounded by Gatekeeper. Know your API SLO.
- Limit scope: exempt namespaces or call the webhook only for some kinds. Dependencies are non-obvious: cluster-scoped Nodes, other critical namespaces like istio-system, even ConfigMaps used as leader-election locks.
- Harden: more webhook pods raises QPS capacity and uptime but may lengthen time for all pods to enforce a new constraint. Pods sharing a failure domain (node, host, switch, power, rack) fail together.

## Checked

2026-11-08. Confirmed against failing-closed.md, read in full (default failurePolicy, example configuration, deadlock, mitigation, availability, scoping gotchas, scaling themes, failure domains). Removed or corrected: said to set Fail only on validation.gatekeeper.sh, but the doc's example sets both webhooks; operator wording aligned to the source.

Method: documentation only; no commands were run.
