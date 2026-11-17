---
id: computing-software.devops-ci-cd.argo-workflows.http-template
name: http-template
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [http-template, success-condition, argo-agent, workflow-task-set, timeout-seconds]
level: practitioner
status: docs-checked
description: "Call HTTP endpoints from a workflow with the http template, its successCondition variables, the result output, and the Argo Agent RBAC it needs."
sources: ["https://argo-workflows.readthedocs.io/en/latest/http-template/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP template
An `http` template makes a request and puts the response body in the `result` output parameter. Fields shown on the page:

```yaml
http:
  timeoutSeconds: 20      # default 30
  url: "{{inputs.parameters.url}}"
  method: "GET"           # default GET
  headers:
    - name: "x-header-name"
      value: "test-value"
  successCondition: "response.body contains \"google\""
  body: "test body"
```

`successCondition` is an expression; the template succeeds only if it is true. Variables: `request.body`, `request.headers`, `request.url`, `request.method`, `response.statusCode` (int), `response.body`, `response.headers` (maps of string lists).

HTTP and Plugin templates run through the Argo Agent, which executes requests independently of the controller. They communicate via the `WorkflowTaskSet` CRD, created for each running Workflow that needs the Agent. You must add workflow RBAC for an agent role; an example agent role is in the quick-start manifests.

Agent failures: each Workflow runs the Agent in one pod. After a container or pod failure the replacement runs every HTTP or Plugin task that has no result yet, so a request can run more than once and should be safe to repeat. The controller replaces a failed pod no sooner than one minute after it was created and records an `AgentPodFailed` Warning event. Set `activeDeadlineSeconds` or a template timeout to bound a task that never gets a result.

Size limit: the `WorkflowTaskSet` holds the full template of every pending or running HTTP and Plugin node, so a wide fan-out can exceed the Kubernetes object size limit; the controller then marks those nodes Error. `parallelism` does not count these nodes; use a template-level semaphore or smaller templates.

## Checked
2026-11-03. Confirmed against the Argo Workflows HTTP Template page: the example fields and defaults, successCondition variables, the Agent and WorkflowTaskSet RBAC note, Agent pod failure behaviour and the WorkflowTaskSet size limit (both added from the page). Removed an uncited claim that the requests never run without the role, an uncited note on hooks and notifications, and a redundant paragraph.
Method: documentation only; no commands were run.
