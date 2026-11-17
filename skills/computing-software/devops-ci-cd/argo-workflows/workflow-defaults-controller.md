---
id: computing-software.devops-ci-cd.argo-workflows.workflow-defaults-controller
name: workflow-defaults-controller
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-defaults, default-workflow-spec, ttl-strategy, controller-configmap, default-values]
level: practitioner
status: docs-checked
description: "Set default Workflow metadata and spec for every Workflow in a controller via workflowDefaults in workflow-controller-configmap."
sources: ["https://argo-workflows.readthedocs.io/en/latest/default-workflow-specs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller workflowDefaults
Put defaults under the `workflowDefaults` key of `workflow-controller-configmap`. It is a YAML string and any value under `Workflow.metadata` or `Workflow.spec` is allowed. They suit config-style fields repeated everywhere, like garbage collection. A value on the Workflow always beats the default.

```yaml
data:
  workflowDefaults: |
    metadata:
      annotations:
        argo: workflows
      labels:
        foo: bar
    spec:
      ttlStrategy:
        secondsAfterSuccess: 5
      parallelism: 3
```

This partially produces a Workflow with those annotations and labels, `ttlStrategy.secondsAfterSuccess: 5` (time to live after success) and `parallelism: 3`.

For the field reference of `ObjectMeta` and `WorkflowSpec`, see fields.md under Workflow.

Per namespace overrides are possible from v4.2 using a labelled ConfigMap; see the namespace defaults skill. Precedence overall is Workflow, then namespace defaults, then these controller defaults.

## Checked

2026-11-08. Read the Argo Workflows default workflow specs page in full (raw markdown) and confirmed workflowDefaults in workflow-controller-configmap, precedence, and the example. Removed: the templateDefaults claim and the list of typical uses, which the page does not state.

Method: documentation only; no commands were run.
