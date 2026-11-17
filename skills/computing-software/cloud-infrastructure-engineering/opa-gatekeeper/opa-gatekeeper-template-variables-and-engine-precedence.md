---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-template-variables-and-engine-precedence
name: opa-gatekeeper-template-variables-and-engine-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, rego, cel, variables, inventory, precedence, k8snativevalidation]
level: advanced
status: docs-checked
description: "Know which variables Rego and CEL policies see in Gatekeeper and which engine wins when a ConstraintTemplate defines more than one."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/constrainttemplates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper template variables and engine precedence

Variables available in Rego policies:
- `input.review`: the request object under review.
- `input.review.namespaceObject`: full Namespace (metadata, labels, annotations) for namespaced resources; null for cluster-scoped ones.
- `input.parameters`: the Constraint parameters.
- `data.lib`: import path for helper functions declared under `libs` in the template.
- `data.inventory`: synced cluster resources, for referential rules such as unique ingress host.

Variables in CEL policies:
- `variables.params`: Constraint parameters.
- `variables.anyObject`: the object, or oldObject on DELETE.
- `namespaceObject`: the Namespace, aligned with Kubernetes Validating Admission Policy.

Precedence: the legacy `spec.targets[].rego` field overrides any Rego engine in `spec.targets[].code[]`. If several engines are in `code`, only one is evaluated: the `K8sNativeValidation` (CEL) engine outranks `Rego`, with no fallback. Best practice is to use only the `code` array and put logic in a single engine: Rego for complex or referential policies and external data, CEL for simpler checks.

## Checked

2026-11-08. Confirmed against constrainttemplates.md, read in full (Built-in variables tables for Rego and CEL, Field Precedence in ConstraintTemplate). Removed or corrected: nothing.

Method: documentation only; no commands were run.
