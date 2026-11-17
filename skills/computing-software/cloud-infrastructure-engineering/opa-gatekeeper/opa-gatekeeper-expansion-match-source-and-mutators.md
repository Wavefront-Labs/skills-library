---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-expansion-match-source-and-mutators
name: opa-gatekeeper-expansion-match-source-and-mutators
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, expansion, match-source, generated, original, istio, mutators]
level: sme
status: docs-checked
description: "Use match.source Generated, Original or All to mimic injected fields such as Istio sidecars on expanded resources without touching real objects."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/expansion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper expansion match source and mutators

Mutators and Constraints have `match.source`: `Generated` applies only to expanded (fake) resources, `Original` only to real ones, and `All` (default) to both. Mutators with `source: Generated` never mutate real cluster resources, so they can mimic what other controllers or webhooks do.

Example: a cluster policy requires an Istio sidecar. Istio injects the sidecar into the created Pods, so the Deployment template lacks it. Add an `ExpansionTemplate` for Deployment to Pod, an `Assign` adding the `istio-proxy` container at `spec.containers[name:istio-proxy]`, and a `ModifySet` with `operation: merge` adding args `proxy` and `sidecar`; the expanded Pod then contains both containers and the constraint can be satisfied.

Constraints can also be limited by source. A policy forbidding standalone Pods but allowing Pods created by workloads uses:

```yaml
spec:
  match:
    source: Original
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
```

Use `Generated` on a constraint to give expanded resources a different treatment than original ones. Note the source is set in `match`, which also lets you separate enforcement actions for expanded and original resources.

## Checked

2026-11-08: read the Configuring Expansion, Match Source and Mutating Example sections of website/docs/expansion.md in the Gatekeeper repo. Confirmed the three source values and default, the Istio example resources and the block-standalone-pods constraint. Reworded: the Istio injection timing, which the page does not state.

Method: documentation only; no commands were run.
