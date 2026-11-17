---
id: computing-software.devops-ci-cd.argo-workflows.lifecycle-hooks
name: lifecycle-hooks
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [lifecycle-hook, hooks, exit-handler, workflow-status, notification]
level: advanced
status: docs-checked
description: "Trigger templates from workflow-level or template-level hooks using expressions on workflow.status, with the rules for exit hooks, errors and unsupported outputs."
sources: ["https://argo-workflows.readthedocs.io/en/latest/lifecyclehook/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lifecycle hooks
A `LifecycleHook` runs a template when an expression becomes true, or on completion, at workflow level (`spec.hooks`) or template level (`hooks` on a step or task). It runs during execution, in parallel with its step, at most once; an expanded step (`withItems`, `withParam`, `withSequence`) runs hooks once per item.

```yaml
spec:
  hooks:
    exit:
      template: http
    running:
      expression: workflow.status == "Running"
      template: http
```

Never name a hook `exit` unless you want an exit handler: that name makes it one. Otherwise the name is irrelevant. An exit handler is effectively a workflow hook whose expression is `workflow.status` equal to Succeeded, Failed or Error.

Supported fields: the exit handler variables `workflow.status` and `workflow.failures`, plus `template`, `templateRef` and `arguments`. Hook arguments referring to outputs of skipped or omitted steps follow the variables page rules.

Unsupported: the hooked step's own `outputs`, since they only exist after completion. Outputs of earlier steps are fine. If you need the outputs, use an exit handler, which has all status variables.

Failure semantics for steps and tasks:
- An exit hook starts only after hooks that already started have finished; dependants wait for all hooks.
- A hook that ends `Error` (could not start, or timed out while `Pending`) fails the DAG or Steps template and `continueOn` does not cover it.
- A hook that ends `Failed` is ignored.

Common use is notification, e.g. an `http` template call on status changes.

## Checked
2026-11-03. Confirmed against the Argo Workflows Lifecycle-Hook page: hook semantics, the exit naming rule, supported and unsupported conditions, the failure rules for steps and tasks, and the notification example. Nothing removed.
Method: documentation only; no commands were run.
