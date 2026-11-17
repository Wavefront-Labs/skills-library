---
id: computing-software.cloud-infrastructure-engineering.cilium.policy-enforcement-modes
name: policy-enforcement-modes
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, policy-enforcement, enable-policy, default-deny, policyenforcementmode]
level: practitioner
status: docs-checked
description: "Choose Cilium policy enforcement mode default, always or never via enable-policy or policyEnforcementMode, plus per-direction default-deny."
sources:
  - https://docs.cilium.io/en/stable/security/policy/intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policy enforcement modes

Goal: decide when endpoints become default-deny.

Modes, set with Helm value `policyEnforcementMode` or agent flag `enable-policy`:
- `default`: endpoints are unrestricted until selected by a policy. Once selected, only allowed traffic passes. State is per direction: a rule that selects the endpoint and has an `ingress` section puts it in ingress default-deny; an `egress` section does the same for egress.
- `always`: enforcement on all endpoints even with no rules. If you want the health entity to check cluster-wide connectivity under `enable-policy: always`, explicitly allow communication to and from the health endpoint.
- `never`: enforcement disabled on all endpoints even when rules select them; all traffic allowed.

## Rule semantics
Rules are a whitelist: each rule allows what it matches. A broader rule wins over a narrower one, intersecting rules allow the union, and anything matching no rule is dropped according to the enforcement mode. A rule with both ingress and egress omitted has no effect.

## Gotcha
The first policy to select an endpoint switches its default mode in that direction, so a single narrow rule can start dropping traffic you did not list.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the policy enforcement modes and rule basics page: https://docs.cilium.io/en/stable/security/policy/intro/. Confirmed the statements above. Nothing was removed.

Method: documentation only; no commands were run.
