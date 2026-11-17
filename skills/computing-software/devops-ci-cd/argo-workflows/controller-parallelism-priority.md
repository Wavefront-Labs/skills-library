---
id: computing-software.devops-ci-cd.argo-workflows.controller-parallelism-priority
name: controller-parallelism-priority
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [parallelism, namespace-parallelism, parallelism-limit, priority, controller-limits]
level: practitioner
status: docs-checked
description: "Cap concurrent Workflows with parallelism and namespaceParallelism in the controller ConfigMap, per-namespace label overrides, and workflow priority queuing."
sources: ["https://argo-workflows.readthedocs.io/en/latest/parallelism/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller parallelism and priority
Controller-level limits sit in the workflow-controller ConfigMap `data`:

```yaml
parallelism: "10"            # all running workflows
namespaceParallelism: "4"    # per namespace
```

Workflows that are executing but blocked from more nodes by another mechanism still count against these limits.

With `namespaceParallelism` enabled, a lower priority workflow can start before a higher one if the higher one's namespace is at its limit.

Per-namespace overrides: put the label `workflows.argoproj.io/parallelism-limit` on the Namespace object. It overrides the global namespace limit. The controller needs get, watch and list permissions on namespaces for this; leaving them out is not an error, the feature just does not work. That omission is reasonable in namespace-scoped installs.

Priority: set `spec.priority: 3` on a Workflow. Workflows held back by controller-level parallelism queue, and higher numbers start first. The default is `priority: 0`.

Other controls (mutexes, semaphores and per-Workflow `parallelism`) live on the synchronization page.

## Checked
2026-11-03. Confirmed against the Argo Workflows Limiting Parallelism page: `parallelism` and `namespaceParallelism` keys, the lower-priority-first caveat, the `workflows.argoproj.io/parallelism-limit` label and its get/watch/list permission requirement, `spec.priority` queuing and the default of 0. Removed a duplicated note.
Method: documentation only; no commands were run.
