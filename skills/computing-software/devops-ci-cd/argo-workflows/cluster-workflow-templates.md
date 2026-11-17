---
id: computing-software.devops-ci-cd.argo-workflows.cluster-workflow-templates
name: cluster-workflow-templates
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [cluster-workflow-template, cluster-scope, template-ref, cluster-template, cwft]
level: practitioner
status: docs-checked
description: "Share templates across all namespaces with cluster-scoped ClusterWorkflowTemplates, referenced using clusterScope true in templateRef and workflowTemplateRef."
sources: ["https://argo-workflows.readthedocs.io/en/latest/cluster-workflow-templates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ClusterWorkflowTemplates
A `ClusterWorkflowTemplate` is a cluster-scoped `WorkflowTemplate`, like a ClusterRole, usable from every namespace. Its spec matches a WorkflowTemplate: `spec.templates`, optionally `entrypoint` and `arguments`.

Reference a template inside one from a `steps` or `dag` template by adding `clusterScope: true`:

```yaml
templateRef:
  name: cluster-workflow-template-print-message
  template: print-message
  clusterScope: true
```

To run a cluster template directly as a Workflow, use `spec.workflowTemplateRef` with `name` and `clusterScope: true`. Arguments you pass in the Workflow are merged with the template's `arguments`. If the Workflow sets nothing else, the template's own `entrypoint` and arguments are used; or set `spec.entrypoint` yourself.

CLI:
- `argo cluster-template create FILE_OR_URL`
- `argo submit --from clusterworkflowtemplate/cluster-workflow-template-submittable`

With kubectl use `kubectl apply -f` and `kubectl get cwft`. They can also be managed from the UI.

## Checked
2026-11-03. Confirmed against the Argo Workflows Cluster Workflow Templates page: cluster scope, `clusterScope: true` in templateRef and workflowTemplateRef, argument merging, the CLI commands and kubectl and UI management. Removed uncited claims about wrong-kind resolution and shared WorkflowTemplate semantics.
Method: documentation only; no commands were run.
