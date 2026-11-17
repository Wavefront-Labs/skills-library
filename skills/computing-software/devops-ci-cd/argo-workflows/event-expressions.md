---
id: computing-software.devops-ci-cd.argo-workflows.event-expressions
name: event-expressions
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [event-expressions, event-payload, event-metadata, x-headers, nil-check]
level: advanced
status: docs-checked
description: "Write correct event selectors over payload, metadata and discriminator, including the lowercase x- header and list-valued header gotchas."
sources: ["https://argo-workflows.readthedocs.io/en/latest/events/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event expression environment
Event expressions (`spec.event.selector` and `valueFrom.event`) are expr expressions over an environment with three names:
- `payload`: the JSON body, e.g. `payload.repository.clone_url == "http://github.com/argoproj/argo"`
- `metadata`: event metadata, including HTTP headers
- `discriminator`: the last URL segment

Because the endpoint accepts any JSON, you must not assume fields exist. Guard with nil checks before dereferencing nested fields.

Header rules in `metadata`:
- Only headers whose names start with `x-` are included.
- Names are lowercased.
- Values are lists, not strings.

Wrong forms include `metadata["X-Github-Event"] == "push"`, `metadata["x-github-event"] == "push"`, `metadata["X-Github-Event"] == ["push"]`, `metadata["github-event"] == ["push"]` and `metadata["authorization"] == ["push"]`. The right form is `metadata["x-github-event"] == ["push"]`. So a selector header name must be written lowercase even if the client sends `X-Argo-E2E`.

`discriminator` is for edge cases where neither payload nor metadata can separate events; usually it should be empty and ignored. Example: `discriminator == "my-discriminator"`.

If an expression is malformed, the Argo Server logs the error and records a `WorkflowEventBindingError` Kubernetes Event on the WorkflowEventBinding; by default the endpoint also returns the error to the caller.

## Checked

2026-11-08. Read the Argo Workflows events page in full (raw markdown) and confirmed the expression environment, payload, header rules, wrong and right header forms, and discriminator. Replaced an unsupported claim about silent failure with the documented malformed-expression behaviour.

Method: documentation only; no commands were run.
