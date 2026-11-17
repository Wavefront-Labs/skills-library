---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-rego-v1-syntax-in-templates
name: opa-gatekeeper-rego-v1-syntax-in-templates
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, rego-v1, opa, code-field, constrainttemplate, syntax]
level: advanced
status: docs-checked
description: "Opt in to Rego v1 syntax in ConstraintTemplates (Gatekeeper 3.19+) using targets.code with engine Rego and source.version v1."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/constrainttemplates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper rego v1 syntax in templates

Gatekeeper 3.19 can evaluate OPA Rego v1 policies, but it is opt-in: by default only Rego v0 is accepted. Use the `code` array instead of the legacy `rego` field, and declare the version:

```yaml
  targets:
    - target: admission.k8s.gatekeeper.sh
      code:
        - engine: Rego
          source:
            version: "v1"
            rego: |
              package k8srequiredlabels
              violation contains {"msg": msg, "details": {"missing_labels": missing}} if {
                provided := {label | input.review.object.metadata.labels[label]}
                required := {label | label := input.parameters.labels[_]}
                missing := required - provided
                count(missing) > 0
                msg := sprintf("you must provide labels: %v", [missing])
              }
```

Rego v1 syntax can only be used under `targets[_].code[_]` with `engine: Rego` and `source.version: "v1"`. You do not need `import rego.v1`. Note the v1 forms: `violation contains {...} if { ... }` replaces the v0 `violation[{...}] { ... }` rule head.

Migration tip: the `code` array and the legacy `rego` field have a defined precedence (the legacy field wins over a Rego engine in `code`), so convert a template by moving its Rego into `code` and removing the old `rego` field in the same change.

## Checked

2026-11-08. Confirmed against constrainttemplates.md, read in full (Enable OPA Rego v1 syntax, field precedence): Gatekeeper 3.19, opt-in, code array with version v1, no import rego.v1 needed, legacy rego field precedence. Removed or corrected: nothing.

Method: documentation only; no commands were run.
