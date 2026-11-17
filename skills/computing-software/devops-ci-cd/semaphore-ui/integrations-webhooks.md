---
id: computing-software.devops-ci-cd.semaphore-ui.integrations-webhooks
name: integrations-webhooks
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [integrations, webhooks, hmac, matchers, value-extractors, semaphore-ui]
level: practitioner
status: docs-checked
description: "Trigger templates from GitHub, Bitbucket or custom webhooks with auth methods, matchers and value extractors."
sources:
  - https://semaphoreui.com/docs/user-guide/integrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Integrations (webhooks)

Goal: start a template when an external service calls Semaphore.

Each integration has a name and a template; the project webhook alias is `/api/integrations/<random_string>` and supports GET and POST. Auth methods: GitHub Webhooks, Bitbucket Webhooks, Token, HMAC (SHA-256), HMAC (SHA-512), BasicAuth, no authentication.

HMAC setup:
1. Set Auth header: the request header carrying the signature (for example `X-Signature` or `X-Hub-Signature-256`).
2. Set Auth secret: a Key Store String key (its value is the secret) or a login/password credential (its password is the secret). BasicAuth needs a login/password credential and checks the login too.

The sender puts the raw hexadecimal HMAC digest of the raw body in the header, without a `sha256=` or `sha512=` prefix:

```bash
SIG="$(printf '%s' "$BODY" | openssl dgst -sha512 -hmac "$SECRET" | awk '{print $2}')"
curl -X POST "https://semaphore.example.com/api/integrations/<alias>" \
  -H "Content-Type: application/json" -H "X-Signature: ${SIG}" --data "$BODY"
```

Matchers define parameters of the incoming request; when they match, the template is invoked. Value extractors take data from a request header or body (JSON field or string) and pass it to the task with a Variable type: Environment (added to the task's environment variables, overriding a same-named variable-group variable) or Task parameter (for example a survey variable or a prompt).

The project alias (the URL above the integration list) is shared by the project; matchers of every integration are checked and all matching templates start. An integration can also have its own alias; requests to it start that integration without evaluating matchers.

Verify: a signed curl call creates a task in the template history.

## Checked

2026-11-04: checked against the integrations page. Corrected matcher and extractor wording to the documented Variable types and added the per-integration alias behaviour.

Method: documentation only; no commands were run.
