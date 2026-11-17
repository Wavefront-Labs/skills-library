---
id: computing-software.devops-ci-cd.argo-workflows.http-agent-failures-and-limits
name: http-agent-failures-and-limits
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [agent-pod-failed, workflow-task-set-size, http-template-limits, active-deadline-seconds, plugin-templates]
level: advanced
status: docs-checked
description: "Understand what happens when the Argo Agent pod fails and how wide HTTP or Plugin fan-outs overflow the WorkflowTaskSet object size limit."
sources: ["https://argo-workflows.readthedocs.io/en/latest/http-template/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Agent failures and WorkflowTaskSet limits
Each Workflow that uses HTTP or Plugin templates runs a single Agent pod.

Failure behaviour:
- If the Agent container exits with an error, the kubelet restarts it and it reruns every HTTP or Plugin task that has no result yet.
- If the pod itself fails (for example node eviction), the controller deletes it and creates a replacement, which also reruns all tasks lacking a result.
- So a request can execute more than once. Make requests idempotent.
- The controller replaces a failed pod no sooner than one minute after its creation, and records an `AgentPodFailed` Warning event with the reason each time.
- Replacements are unlimited. A task that never gets a result fails via the Workflow `activeDeadlineSeconds`, or via template `timeout` unless the plugin already reported it `Running`. With neither, it can run until something else stops the Workflow.
- When the Workflow is stopping, terminating or past its deadline, the controller errors those nodes instead.

Size limit: the WorkflowTaskSet stores the full template of every pending or running HTTP and Plugin node. A wide fan-out can exceed the Kubernetes object limit (about 1.5 MiB with default etcd). Then the controller marks every such node `Error` with a message naming the size limit, even ones that would have fit, while tasks already stored keep running.

`parallelism` does not count HTTP or Plugin nodes, so it cannot cap this. Use a template-level semaphore to reduce simultaneous nodes, or shrink the templates.

## Checked
2026-11-08. Confirmed against the Argo Workflows HTTP Template page: Agent pod failure and restart behaviour, the one-minute replacement delay, the `AgentPodFailed` event, `activeDeadlineSeconds` and template `timeout` handling, the WorkflowTaskSet size limit (about 1.5 MiB), and that `parallelism` does not count HTTP or Plugin nodes. Nothing removed.
Method: documentation only; no commands were run.
