---
id: computing-software.devops-ci-cd.argo-workflows.workflow-event-binding
name: workflow-event-binding
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-event-binding, events-endpoint, discriminator, submit-metadata, event-selector]
level: practitioner
status: docs-checked
description: "Trigger a WorkflowTemplate from a JSON event via the Argo Server events endpoint and a WorkflowEventBinding, with argument mapping and naming."
sources: ["https://argo-workflows.readthedocs.io/en/latest/events/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WorkflowEventBinding submit
Post any JSON to `/api/v1/events/{namespace}/{discriminator}` on the Argo Server (note the trailing slash when the discriminator is empty), with an access token in the `Authorization` header. This is unrelated to Argo Events. By default the endpoint processes the event before it returns and can report failures. With `--event-async-dispatch` it queues the event and returns at once, so failures are not reported synchronously and it returns 503 if the queue is full. Processing order is not guaranteed.

Create the WorkflowTemplate first, then bind it:

```yaml
kind: WorkflowEventBinding
spec:
  event:
    selector: payload.message != "" && metadata["x-argo-e2e"] == ["true"] && discriminator == "my-discriminator"
  submit:
    workflowTemplateRef:
      name: my-wf-tmple
    arguments:
      parameters:
      - name: message
        valueFrom:
          event: payload.message
```

The token can only submit templates its role allows. A malformed expression is logged by the Argo Server and recorded as a `WorkflowEventBindingError` Kubernetes Event on the WorkflowEventBinding; by default the endpoint also returns the error.

Customise the created Workflow with `submit.metadata`: `name`, `annotations` and `labels` values are all expressions, so quote them in single quotes, e.g. `name: 'event.payload.message + "-world"'` and `someLabel: '"literal string"'`. Default name is the template name plus a random suffix. If the name evaluates to an existing Workflow, the submit fails. Results must be strings obeying Kubernetes naming rules.

## Checked
2026-11-08. Confirmed against the Argo Workflows Events page: endpoint path and trailing slash, async dispatch and 503 behaviour, the WorkflowEventBinding selector and argument example, lowercase `x-` header names, `submit.metadata` expressions, the random-suffix default name and name clash failure. Corrected the always-async claim, the 10 second claim, the default name and the malformed-expression behaviour.
Method: documentation only; no commands were run.
