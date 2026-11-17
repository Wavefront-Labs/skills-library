---
id: computing-software.devops-ci-cd.argo-workflows.workflow-templates-reuse
name: workflow-templates-reuse
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-template, template-ref, workflow-template-ref, workflow-metadata, global-parameters]
level: practitioner
status: docs-checked
description: "Reuse WorkflowTemplates through templateRef inside steps or dag and workflowTemplateRef at Workflow level, with parameter scoping rules and workflowMetadata labels."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-templates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WorkflowTemplate reuse with templateRef
A `WorkflowTemplate` is a Workflow definition stored in the cluster; a lowercase `template` is a unit inside `templates`. Any Workflow can become a WorkflowTemplate by changing `kind`. All `WorkflowSpec` fields work except `priority`, which must be set on a Workflow's own spec. `spec.workflowMetadata.labels` and `annotations` get stamped on Workflows created from it.

Call a template from another WorkflowTemplate with `templateRef` (`name` of the resource plus `template` name) and pass `arguments` as usual. Only do this from a `steps` or `dag` template.

Run a whole WorkflowTemplate as a Workflow with `spec.workflowTemplateRef.name`. Arguments given on the Workflow are merged with the template's arguments, and `entrypoint` may be supplied by either side.

Parameter rules:
- Global parameters: set under the Workflow's `spec.arguments` and read in the template as `{{workflow.parameters.global-parameter}}`.
- Local parameters: a value must be supplied inside the WorkflowTemplate at the template's `inputs.parameters`.

CLI: `argo template create FILE`, `argo submit --from workflowtemplate/NAME -p message=value1`. Parameters passed this way need not be declared by the template, so it can reference `{{workflow.parameters.name}}` for values that have no sensible default. `kubectl get wftmpl` lists them.

UI tip: add `enum` under a parameter in `spec.arguments.parameters` (with a `value`) to get a drop-down when submitting.

## Checked

2026-11-08. Read the Argo Workflows workflow templates page in full (raw markdown) and confirmed templateRef, workflowTemplateRef, argument merging, parameter rules, workflowMetadata, CLI submit, and enum drop-downs. Nothing removed.

Method: documentation only; no commands were run.
