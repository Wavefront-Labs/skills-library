---
id: computing-software.devops-ci-cd.argo-workflows.workflow-inputs-and-outputs
name: workflow-inputs-and-outputs
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-inputs, arguments, inputs-parameters, artifact-from, parameter-description]
level: intro
status: docs-checked
description: "Wire workflow arguments into template inputs and pass parameters and artifacts between DAG tasks (value vs from), with parameter descriptions."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-inputs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow inputs and passing outputs
A Workflow supplies `arguments` to its entry point; a template declares `inputs`; callers (`steps`, `dag`, or the Workflow) provide them. Both use the same structure:

```yaml
arguments:
  parameters:
  - name: workflow-param-1
```

A DAG task passes values in `arguments.parameters`, e.g. `value: "{{workflow.parameters.workflow-param-1}}"`, and the template reads `{{inputs.parameters.template-param-1}}`. Override at submit time with `argo submit -n argo example.yaml -p 'workflow-param-1="abcd"' --watch`.

Using an earlier task's output (declared under `outputs.parameters` with `valueFrom.path`, and `outputs.artifacts` with `path`):

```yaml
arguments:
  parameters:
  - name: template-param-2
    value: "{{tasks.step-A.outputs.parameters.output-param-1}}"
  artifacts:
  - name: input-artifact-1
    from: "{{tasks.step-A.outputs.artifacts.output-artifact-1}}"
```

Gotcha: parameters and artifacts both have `name`, but a parameter uses `value` whereas an artifact uses `from`. In the docs example the consuming task lists the producer in `dependencies`.

Add `description` to a parameter to show a tooltip in the UI when submitting or providing intermediate inputs. It supports Markdown (bold, italic, code, links, line breaks).

The submit example runs in namespace `argo` with `--watch` to follow progress. Terms such as arguments, inputs and templates are defined in the Core Concepts glossary.

## Checked
2026-11-08. Confirmed against the Argo Workflows Workflow Inputs page: arguments and inputs structure, the DAG arguments example, the `argo submit` command, parameter `value` versus artifact `from`, and parameter `description` with Markdown. Softened the dependencies statement to what the example shows.
Method: documentation only; no commands were run.
