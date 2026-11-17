---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-vap-cel-engine-k8snativevalidation
name: opa-gatekeeper-vap-cel-engine-k8snativevalidation
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, validating-admission-policy, cel, k8snativevalidation, engines, gator, anyobject]
level: advanced
status: docs-checked
description: "Write Gatekeeper ConstraintTemplates in CEL using the K8sNativeValidation engine and understand engine priority and the anyObject variable."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/validating-admission-policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper vap cel engine k8snativevalidation

Gatekeeper (stable for CEL validation since v3.18; needs v3.17 minimum) can evaluate Kubernetes Validating Admission Policy (VAP) style CEL inside ConstraintTemplates, so one policy works in the Gatekeeper webhook, audit and the gator CLI even on clusters without VAP. Disable with `--enable-k8s-native-validation=false`.

Enforcement options by language:
- CEL: webhook, audit, gator, and the Kubernetes built-in admission controller (VAP).
- Rego: webhook, audit, gator, especially for referential policies and external data (Rego is not available as native VAP).

Engine rules from the FAQ: only one engine is evaluated per template; `K8sNativeValidation` outranks `Rego`; there is no fallback and engine priority cannot be changed. A logical or syntax error in policy logic is treated as a violation according to the enforcement action. CEL reads constraint parameters through `variables.params`; the `anyObject` variable exists because Gatekeeper sets Object to oldObject on DELETE whereas Kubernetes VAP does not, so evaluation matches in both environments.

Prerequisites for VAP enforcement: Kubernetes 1.30 (GA); on 1.29 enable the `ValidatingAdmissionPolicy` feature gate and `admissionregistration.k8s.io/v1beta1`.

## Checked

2026-11-04. Confirmed against validating-admission-policy.md (prerequisites, enforcement table, FAQs). Removed or corrected: the unconfirmed `variables.anyObject` spelling.

Method: documentation only; no commands were run.
