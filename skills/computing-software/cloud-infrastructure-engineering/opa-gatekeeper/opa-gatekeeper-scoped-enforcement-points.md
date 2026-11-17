---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-scoped-enforcement-points
name: opa-gatekeeper-scoped-enforcement-points
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, scoped, enforcement-points, gator, vap, audit, validation-webhook]
level: advanced
status: docs-checked
description: "Use enforcementAction scoped with scopedEnforcementActions to choose different actions at the webhook, gator, audit and VAP enforcement points."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/enforcement-points.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper scoped enforcement points

Enforcement points name where a constraint is evaluated:
- `validation.gatekeeper.sh`: the validating admission webhook (CEL and Rego templates).
- `gator.gatekeeper.sh`: shift-left checks via the gator CLI (CEL and Rego).
- `audit.gatekeeper.sh`: audit of on-cluster resources (CEL and Rego).
- `vap.k8s.io`: Kubernetes Validating Admission Policy (CEL templates only).

By default a constraint applies its `spec.enforcementAction` at every point. To vary it, set `enforcementAction: scoped` and list `scopedEnforcementActions`; without `scoped` that list is ignored.

Deny in CI but only warn in cluster:

```yaml
spec:
  enforcementAction: scoped
  scopedEnforcementActions:
    - action: warn
      enforcementPoints:
        - name: "validation.gatekeeper.sh"
    - action: deny
      enforcementPoints:
        - name: "gator.gatekeeper.sh"
```

Other documented patterns: audit-only (just `audit.gatekeeper.sh`) for latency-sensitive external-data or referential policies; `vap.k8s.io` plus `validation.gatekeeper.sh` so Gatekeeper backstops a fail-open VAP; `vap.k8s.io` plus `audit.gatekeeper.sh` to enforce in-tree and still audit with Gatekeeper. The audit point is not included unless named explicitly or the points list is `"*"`.

## Checked

2026-11-08. Confirmed against enforcement-points.md, read in full: four enforcement point names and template support, scoped behaviour and ignored list, the four example patterns, audit point exclusion unless named or wildcard. Removed or corrected: nothing.

Method: documentation only; no commands were run.
