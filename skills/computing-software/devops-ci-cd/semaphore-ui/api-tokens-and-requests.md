---
id: computing-software.devops-ci-cd.semaphore-ui.api-tokens-and-requests
name: api-tokens-and-requests
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [api, api-token, bearer-token, swagger, rest, semaphore-ui]
level: practitioner
status: docs-checked
description: "Authenticate to the Semaphore REST API with a bearer API token and find the Swagger and Postman docs."
sources:
  - https://semaphoreui.com/docs/reference/api
  - https://semaphoreui.com/docs/admin-guide/cicd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Semaphore REST API

Goal: call Semaphore programmatically.

Reference: Swagger/OpenAPI at semaphoreui.com/api-docs, an official Postman collection, and Swagger UI built into every instance (the API Reference link on the API Tokens page).

Token: every request carries

```http
Authorization: Bearer YOUR_API_TOKEN
```

Create the token in the web UI (since 2.14): account menu at the bottom of the sidebar, API Tokens, New Token, enter a name and expiry, and copy the value shown once. Alternatively log in over HTTP to obtain a session token.

Example: start a task for template 5 in project 1:

```bash
curl -X POST https://semaphore.example.com/api/project/1/tasks \
  -H 'Authorization: Bearer YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"template_id": 5, "message": "Triggered by CI"}'
```

The response contains the task ID; poll `GET /api/project/1/tasks/{task_id}` until the status is final.

Gotchas:
- To pass an Ansible limit via API, enable the Limit prompt on the template or the value is ignored.
- Rejected tokens and denied requests appear in the audit log.
- Metrics use a separate Basic Auth, not these tokens.

Verify: the task-start call above returns a task whose ID you can poll to a final status.

## Checked

2026-11-04: checked against the API reference and CI/CD pages. Replaced the unconfirmed /api/projects verify call with a check based on the documented task-start call.

Method: documentation only; no commands were run.
