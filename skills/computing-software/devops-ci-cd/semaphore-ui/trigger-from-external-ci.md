---
id: computing-software.devops-ci-cd.semaphore-ui.trigger-from-external-ci
name: trigger-from-external-ci
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [ci-cd, github-actions, gitlab-ci, jenkins, trigger, webhook, semaphore-ui]
level: practitioner
status: docs-checked
description: "Start Semaphore tasks from GitHub Actions, GitLab CI or Jenkins with an integration webhook or the REST API."
sources:
  - https://semaphoreui.com/docs/admin-guide/cicd
  - https://semaphoreui.com/docs/user-guide/tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trigger Semaphore from an external pipeline

Goal: make Semaphore a step in another CI system.

Two ways to start a task from GitHub Actions, GitLab CI, Jenkins or any other system:
1. Integrations: a webhook URL per project that starts a template when the request matches. Supports GitHub signatures, tokens and HMAC, and can pass request fields to the task as variables (see the integrations skill).
2. REST API: create a task with an API token.

```bash
curl -X POST https://semaphore.example.com/api/project/1/tasks \
  -H 'Authorization: Bearer YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"template_id": 5, "message": "Triggered by CI"}'
```

The response contains the task ID. Poll `GET /api/project/1/tasks/{task_id}` until `status` is `success`, `error` or `stopped`, and fail the pipeline unless it is `success`. The API reference has tokens and the built-in Swagger.

Inside Semaphore, Build and Deploy template types give a simple internal pipeline, with the `semaphore_vars` variable (see the build and deploy skill); multi-step pipelines with approvals use Workflows.

Tips:
- Keep the API token in the CI system's secret store, not in the repository.
- Starting a task needs the Task Runner role or higher in the project.

## Checked

2026-11-07. Read in full: the CI/CD integration page (admin-guide/cicd.md in the semaphore-docs repository). Read only the opening lines of user-guide/tasks.md (the Task Runner role statement); the rest of that page and the Integrations and Build and deploy pages were not read. Confirmed: the two trigger routes, the curl example, polling and the three final statuses, semaphore_vars, Workflows, the Task Runner role. Removed: "dedicated user so a leaked token cannot change settings", the audit-log trigger tip, and the invented Verify step.
Method: documentation only; no commands were run.
