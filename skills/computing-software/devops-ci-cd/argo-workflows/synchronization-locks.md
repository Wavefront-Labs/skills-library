---
id: computing-software.devops-ci-cd.argo-workflows.synchronization-locks
name: synchronization-locks
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [synchronization, mutex, semaphore, configmap-key-ref, queue-priority]
level: practitioner
status: docs-checked
description: "Limit concurrent Workflows or Templates with mutexes and ConfigMap semaphores at workflow or template level, including lock namespaces, queue order and multiple locks."
sources: ["https://argo-workflows.readthedocs.io/en/latest/synchronization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutexes and semaphores
Locks limit parallel Workflows or Templates; `parallelism` limits tasks within one Workflow. A mutex allows one holder; a semaphore allows N.

Workflow level, under `spec.synchronization`:
```yaml
synchronization:
  mutexes:
    - name: bar
  semaphores:
    - configMapKeyRef:
        name: my-config
        key: workflow
```
Semaphore size comes from the ConfigMap value (for example `workflow: "1"`, `template: "2"`). The controller watches that ConfigMap, so it needs read permission and size changes apply live. Template level uses the same `synchronization` block on a template, and applies even across steps and different Workflows that use that template.

A lock is identified by namespace plus key. The key is the mutex `name` or the semaphore key; the namespace defaults to the Workflow's namespace but the `namespace` field overrides it, letting namespaces share a common ConfigMap.

Waiting Workflows queue by `priority` (higher number first), then creation time (older first). Only the front of the queue may acquire a lock.

Several locks can be listed together; the Workflow blocks until all are free. Warning: a Workflow at the head of the queue that needs multiple locks makes every other Workflow wanting any of those locks wait, even if they need only a subset.

Inspect state in `.status.synchronization` of the Workflow.

## Checked

2026-11-08. Read the Argo Workflows synchronization page in full (raw markdown) and confirmed mutex and semaphore syntax, ConfigMap sizing, namespace and key rules, queue ordering, multiple lock warning, and .status.synchronization. Nothing removed.

Method: documentation only; no commands were run.
