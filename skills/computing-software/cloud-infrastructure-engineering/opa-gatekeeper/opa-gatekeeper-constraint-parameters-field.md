---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-constraint-parameters-field
name: opa-gatekeeper-constraint-parameters-field
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, constraint, parameters, input-parameters, schema, validation]
level: practitioner
status: docs-checked
description: "Pass policy intent to Rego through Constraint parameters, validated against the ConstraintTemplate schema, and read them as input.parameters."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/howto.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper constraint parameters field

The `parameters` field of a Constraint expresses its intent, much like arguments to a function. Gatekeeper exposes them in the template's Rego as `input.parameters`:

```yaml
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["gatekeeper"]
```

with Rego `required := {label | label := input.parameters.labels[_]}`.

The schema for `parameters` is defined once in the ConstraintTemplate (`openAPIV3Schema`). The API server rejects a Constraint whose parameters do not match, for example sending an array where an object is required returns `spec.parameters: Invalid value: "array": spec.parameters in body must be of type object`.

Another field on the Constraint, `enforcementAction`, defaults to `deny`; `dryrun` and `warn` are the other supported values (see the violations handling skill).

The policy library shows the same pattern in practice: the allowed-repos template reads `input.parameters.repos`, and the required-labels CEL variant reads `variables.params.labels`. In CEL policies the parameters are exposed as `variables.params` rather than `input.parameters`.

## Checked

2026-11-08. Confirmed against howto.md (The parameters field, The enforcementAction field; read in full) and constrainttemplates.md (CEL variables table, policy library examples). Removed or corrected: unsourced claim about serving many constraints per namespace group.

Method: documentation only; no commands were run.
