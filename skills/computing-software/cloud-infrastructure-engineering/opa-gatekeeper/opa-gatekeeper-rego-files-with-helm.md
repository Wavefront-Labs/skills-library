---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-rego-files-with-helm
name: opa-gatekeeper-rego-files-with-helm
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, helm, rego, opa-test, opa-fmt, files-get, unit-testing]
level: advanced
status: docs-checked
description: "Keep Gatekeeper Rego in separate .rego files and inline them into ConstraintTemplates with Helm Files.Get so you can run opa fmt and opa test."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/constrainttemplates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper rego files with helm

For many or complex policies, avoid pasting Rego into YAML. Keep each policy in its own `.rego` file so `opa fmt` and `opa test` work on it, then let Helm inline the file when you install or upgrade the chart.

Chart template `templates/constrainttemplate.yaml`:

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
        {{ .Files.Get "policies/requiredlabels.rego" | indent 8 }}
```

The `indent 8` keeps the inlined Rego aligned under the block scalar. The file `policies/requiredlabels.rego` then lives beside its unit tests in the same repository, so the policy and its tests version together and CI can run `opa test` before the chart is released.

Note that the example uses the legacy `rego` field. That field takes precedence over any Rego engine in `targets[].code[]`, so if you adopt the `code` array (for Rego v1 syntax or CEL) inline the file inside the `source.rego` value there and remove the old field to avoid it shadowing the new entry.

## Checked

2026-11-08. Confirmed against constrainttemplates.md, read in full (Managing Rego at Scale with Helm, field precedence): Files.Get with indent 8, opa fmt and opa test rationale, legacy rego field precedence over code. Removed or corrected: nothing.

Method: documentation only; no commands were run.
