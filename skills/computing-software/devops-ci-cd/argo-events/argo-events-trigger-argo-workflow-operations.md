---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-argo-workflow-operations
name: argo-events-trigger-argo-workflow-operations
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, argoworkflow-trigger, workflow, submit, operation, rbac, operate-workflow-sa]
level: practitioner
status: docs-checked
description: "Use the argoWorkflow trigger to submit or manage Argo Workflows from events, choosing the operation and granting the Sensor RBAC."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/argo-workflow.md", "https://github.com/argoproj/argo-events/blob/master/docs/service-accounts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger argo workflow operations

The Argo Workflow trigger needs Argo Workflows installed. A working recipe from the docs:
1. Have an EventBus in the namespace.
2. Create the service account the Sensor uses, `operate-workflow-sa`, from `examples/rbac/sensor-rbac.yaml`, and reference it in the Sensor as `spec.template.serviceAccountName`.
3. Create a webhook EventSource and a Sensor such as `special-workflow-trigger-shortened.yaml`.
4. Port-forward the EventSource pod (`kubectl -n argo-events port-forward <pod> 12000:12000`), POST to `/example`, and check with `argo list`.

The trigger can drive more than submission. Set `argoWorkflow.operation` to one of: `submit`, `submit-from`, `resubmit`, `resume`, `retry`, `suspend`, `terminate` or `stop`, matching Argo CLI commands.

```yaml
triggers:
  - template:
      name: argo-workflow-trigger
      argoWorkflow:
        operation: submit
        source:
          resource:
            apiVersion: argoproj.io/v1alpha1
            kind: Workflow
            metadata:
              generateName: workflow-template-print-message-
            spec:
              workflowTemplateRef:
                name: workflow-template-print-message
```

Using `workflowTemplateRef` submits a Workflow that points at an existing `WorkflowTemplate`, so steps need not be repeated in the Sensor. Parameterization fills workflow values from the event, and the trigger `policy` decides whether to stop or continue based on the workflow status. A GitHub-webhook end-to-end tutorial exists as tutorial 08.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/argo-workflow.md and docs/service-accounts.md. Confirmed: setup steps, operation list, workflowTemplateRef example, parameterization, policy, tutorial 08 pointer, spec.template.serviceAccountName. Removed or changed: nothing; service-accounts.md added to sources because it (not the trigger page) states the serviceAccountName field. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
