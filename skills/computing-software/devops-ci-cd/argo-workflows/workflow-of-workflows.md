---
id: computing-software.devops-ci-cd.argo-workflows.workflow-of-workflows
name: workflow-of-workflows
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-of-workflows, resource-template, child-workflows, success-condition, failure-condition]
level: advanced
status: docs-checked
description: "Launch child Workflows from a parent using a resource template with action create and wait on their phase with successCondition and failureCondition."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-of-workflows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow of workflows
A parent Workflow creates child Workflows and acts on the results. Steps:

1. Define the child as a WorkflowTemplate with `entrypoint` and `arguments` (for example `workflow-template-submittable`) and create it with `argo template create <yaml>`.
2. In the parent, use a `resource` template per child:

```yaml
- name: resource-with-argument
  inputs:
    parameters:
      - name: workflowtemplate
      - name: message
  resource:
    action: create
    manifest: |
      apiVersion: argoproj.io/v1alpha1
      kind: Workflow
      metadata:
        generateName: workflow-of-workflows-2-
      spec:
        arguments:
          parameters:
          - name: message
            value: {{inputs.parameters.message}}
        workflowTemplateRef:
          name: {{inputs.parameters.workflowtemplate}}
    successCondition: status.phase == Succeeded
    failureCondition: status.phase in (Failed, Error)
```

The child Workflow is the manifest, referencing the template with `workflowTemplateRef`. `successCondition` and `failureCondition` watch the child's `status.phase` so the parent step finishes only when the child does. Variants without `arguments` omit that block.

Steps in the parent (`steps` or `dag`) pass the template name and arguments as parameters, so one resource template can be reused for several children.

## Checked

2026-11-08. Read the Argo Workflows workflow of workflows page in full (raw markdown) and confirmed the WorkflowTemplate plus resource template pattern, success and failure conditions, and the reusable resource template. Removed: the service account permission claim and the etcd size limit remark, which the page does not state.

Method: documentation only; no commands were run.
