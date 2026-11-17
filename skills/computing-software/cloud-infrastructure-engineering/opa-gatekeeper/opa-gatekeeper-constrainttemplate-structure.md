---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-constrainttemplate-structure
name: opa-gatekeeper-constrainttemplate-structure
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, constrainttemplate, constraint, rego, crd, validation, policy-model]
level: intro
status: docs-checked
description: "Understand how a Gatekeeper ConstraintTemplate pairs Rego or CEL violation logic with a parameter schema that generates a Constraint CRD."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/howto.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper constrainttemplate structure

Gatekeeper validation uses two resources. A `ConstraintTemplate` defines both the policy code and the schema of its parameters; a `Constraint` (an instance of the kind the template names) says where and how to apply it. Mutation policies use separate mutator resources.

Example template requiring labels:

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels: {type: array, items: {type: string}}
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("you must provide labels: %v", [missing])
        }
```

`spec.crd.spec.names.kind` becomes the Constraint kind. The `openAPIV3Schema` describes the Constraint `parameters` field, like arguments to a function. In the example the Rego package defines a `violation` rule that returns a `msg` and `details`.

## Checked

2026-11-08. Confirmed against howto.md (Constraint Templates and Constraints sections; read in full) and cross-read constrainttemplates.md: template and constraint roles, v1 apiVersion, names.kind, openAPIV3Schema as parameters schema, mutation pointer. Removed or corrected: the general statement that the package must define violation rules returning msg, now limited to what the example shows.

Method: documentation only; no commands were run.
