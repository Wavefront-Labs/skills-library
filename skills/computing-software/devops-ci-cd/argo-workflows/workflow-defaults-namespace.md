---
id: computing-software.devops-ci-cd.argo-workflows.workflow-defaults-namespace
name: workflow-defaults-namespace
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [namespace-defaults, workflow-defaults-configmap, configmap-type, template-referencing, per-namespace-defaults]
level: advanced
status: docs-checked
description: "Give each namespace its own workflowDefaults through a ConfigMap labelled workflows.argoproj.io/configmap-type WorkflowDefaults (v4.2 and later), with the error cases to avoid."
sources: ["https://argo-workflows.readthedocs.io/en/latest/default-workflow-specs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespace level workflow defaults
From v4.2 a ConfigMap in the Workflows' namespace can carry `data.workflowDefaults` (same shape as the controller one) and the label `workflows.argoproj.io/configmap-type: WorkflowDefaults`. The controller finds it by label, so the name is free.

```yaml
metadata:
  name: my-workflow-defaults
  labels:
    workflows.argoproj.io/configmap-type: WorkflowDefaults
data:
  workflowDefaults: |
    spec:
      serviceAccountName: my-namespace-sa
      ttlStrategy:
        secondsAfterCompletion: 60
```

Precedence is Workflow, then namespace defaults, then controller `workflowDefaults`, merged rather than replaced.

Allowed: `spec` fields plus labels and annotations under `metadata`; other metadata and `status` are ignored. A label with the `workflows.argoproj.io/` prefix is an error, because a completed label would make new Workflows look finished.

Error cases (each puts affected Workflows into `Error`, including running ones, since defaults are re-read on each reconcile):
- two labelled ConfigMaps in one namespace
- missing `workflowDefaults` key, invalid YAML, or an unrecognised field
- under `templateReferencing: Secure`, any edit that changes the merged spec of a running `workflowTemplateRef` Workflow

Trust: `templateReferencing: Strict` does not restrict namespace defaults, so such a ConfigMap can set `serviceAccountName`, `hostNetwork` or `podSpecPatch`. Write access to it equals controller-level trust. A Workflow using a ClusterWorkflowTemplate gets defaults of the namespace it runs in.

## Checked

2026-11-08. Read the Argo Workflows default workflow specs page in full (raw markdown) and confirmed the namespace ConfigMap label, precedence, allowed fields, error cases, Strict and Secure behaviour, and trust note. Nothing removed.

Method: documentation only; no commands were run.
