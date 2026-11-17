---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-expansion-template-workload-validation
name: opa-gatekeeper-expansion-template-workload-validation
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, expansiontemplate, workload, generatedgvk, templatesource, expansion, beta]
level: advanced
status: docs-checked
description: "Reject Deployments and other workloads whose Pods would violate constraints by defining an ExpansionTemplate that expands them into temporary Pods."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/expansion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper expansion template workload validation

`ExpansionTemplate` (alpha v3.10, beta v3.13+, enabled by default; disable with `enable-generator-resource-expansion=false`) makes Gatekeeper build temporary "expanded resources" from a parent workload and validate constraints against them. It specifies the parent GVKs (`applyTo`), the child (`generatedGVK`), the blueprint path in the parent (`templateSource`, typically `spec.template`), and an optional `enforcementAction` override applied only to violations on expanded resources.

```yaml
apiVersion: expansion.gatekeeper.sh/v1alpha1
kind: ExpansionTemplate
metadata:
  name: expand-deployments
spec:
  applyTo:
    - groups: ["apps"]
      kinds: ["DaemonSet", "Deployment", "ReplicaSet", "StatefulSet"]
      versions: ["v1"]
  templateSource: "spec.template"
  enforcementAction: "warn"
  generatedGVK:
    kind: "Pod"
    group: ""
    version: "v1"
```

Constraints that target Pods are then also evaluated on the expanded Pods when a Deployment is reviewed, by both the webhook and audit. Test with `gator expand`.

Limits: the expansion cannot be fully accurate (random pod names, sidecars injected by other webhooks, request-time metadata such as requesting user), which can cause over- or under-enforcement.

## Checked

2026-11-04. Confirmed against expansion.md (feature state, ExpansionTemplate fields, limitations). Removed or corrected: nothing.

Method: documentation only; no commands were run.
