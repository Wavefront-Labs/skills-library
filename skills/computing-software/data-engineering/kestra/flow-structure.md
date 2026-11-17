---
id: computing-software.data-engineering.kestra.flow-structure
name: flow-structure
category: computing-software
field: data-engineering
product: kestra
tags: [flow, yaml, namespace, revisions, draft, flow-properties]
level: intro
status: docs-checked
description: "Anatomy of a Kestra flow: required id, namespace and tasks, optional top-level properties, revisions and drafts, and the flow context variables."
sources:
  - https://kestra.io/docs/workflow-components/flow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A flow is a container for tasks and their orchestration logic, written in YAML or built in the No Code editor.

Required: `id`, `namespace`, `tasks`.

Optional: `inputs`, `outputs`, `variables`, `triggers`, `labels`, `errors`, `finally`, `retries`, `sla`, `concurrency`, `description` (Markdown), `disabled`, `checks`.

```yaml
id: hello-world
namespace: company.team

tasks:
  - id: hello
    type: io.kestra.plugin.core.log.Log
    message: "Hello, {{ inputs['my-value'] }}!"
```

Revisions:

- Every change creates a revision, listed in the Revisions tab.
- Save as draft stages changes without affecting running executions.
- Drafts do not run; triggers and manual runs use the last published revision until you publish.

Flow context expressions: `{{ flow.id }}`, `{{ flow.namespace }}`, `{{ flow.revision }}`, and `{{ flow.tenantId }}` (Enterprise Edition and Cloud only).

## Checked

2026-11-04. Confirmed against the Kestra flow page: required id, namespace and tasks, the optional property list, revisions, save as draft falling back to the last published revision, flow context expressions with tenantId EE and Cloud only. Nothing removed.

Method: documentation only; no commands were run.
