---
id: computing-software.devops-ci-cd.argo-workflows.template-defaults
name: template-defaults
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [template-defaults, strategic-merge-patch, default-timeout, default-retry-strategy, patch-merge-key]
level: practitioner
status: docs-checked
description: "Apply shared template values with spec.templateDefaults at workflow or controller level, merged by Kubernetes strategic merge patch with template values winning."
sources: ["https://argo-workflows.readthedocs.io/en/latest/template-defaults/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template defaults
`spec.templateDefaults` sets values applied to every template in the Workflow, such as `timeout` and `retryStrategy`:

```yaml
spec:
  entrypoint: main
  templateDefaults:
    timeout: 30s
    retryStrategy:
      limit: 2
```

If a template defines the same field, the template's value takes precedence. Merging happens at runtime using Kubernetes strategic merge patch. To learn whether list fields are merged or replaced, inspect the `patchStrategy` and `patchMergeKey` tags in the workflow definition.

Controller level: operators put templateDefaults under `workflowDefaults` in the `workflow-controller-configmap`, so they apply to all Workflows run by that controller:

```yaml
data:
  workflowDefaults: |
    spec:
      ttlStrategy:
        secondsAfterSuccess: 5
      templateDefaults:
        timeout: 30s
```

The controller values apply unless overridden at Workflow level. The Scaling page also uses `templateDefaults.metadata.labels` to stamp an instance ID label (`workflows.argoproj.io/controller-instanceid`) on templates of a WorkflowTemplate.

## Checked
2026-11-03. Confirmed against the Argo Workflows Template Defaults page (workflow and controller level examples, precedence, strategic merge patch) and the Scaling page (instance ID labels). Removed uncited references to a Go source file name and an examples file, and an uncited three-way override claim.
Method: documentation only; no commands were run.
