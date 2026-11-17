---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-v1-templates-structural-schema
name: opa-gatekeeper-v1-templates-structural-schema
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, v1, structural-schema, openapiv3schema, validation, parameters, upgrade]
level: practitioner
status: docs-checked
description: "Fix ConstraintTemplate v1 migrations by adding type information to the parameters schema so the API server rejects malformed Constraint parameters."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/constrainttemplates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper v1 templates structural schema

Since Gatekeeper 3.6.0, `templates.gatekeeper.sh/v1` requires the Constraint schema (`spec.crd.spec.validation.openAPIV3Schema`) to be structural: every level must declare `type`. A v1beta1 template whose schema starts with `properties:` and no `type: object` is invalid in v1; add `type: object` at the top.

Why it matters: in v1beta1 a mistyped Constraint such as

```yaml
parameters:
  - labels: ["gatekeeper"]   # array item instead of object key
```

was accepted by the API server, but Gatekeeper never received the parameters, so `kubectl create ns foobar` succeeded without the required label. With a structural schema the API server rejects it immediately: `spec.parameters in body must be of type object: "array"`. Fixing the YAML to `parameters: {labels: ["gatekeeper"]}` gives a working constraint, and creating the namespace is then denied with `[ns-must-have-gk] you must provide labels: {"gatekeeper"}`.

Structural schemas follow the Kubernetes CRD rules, so other CRD restrictions apply; this alignment with `CustomResourceDefinition` v1 also makes the Constraint schema more visible and type-validated.

## Checked

2026-11-08. Confirmed against constrainttemplates.md, read in full (v1 Constraint Template, Why implement this change): 3.6.0 introduction, structural schema and type requirement, v1beta1 silent acceptance example, rejection message, denial message. Removed or corrected: nothing.

Method: documentation only; no commands were run.
