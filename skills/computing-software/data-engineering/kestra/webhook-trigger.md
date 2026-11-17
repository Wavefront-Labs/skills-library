---
id: computing-software.data-engineering.kestra.webhook-trigger
name: webhook-trigger
category: computing-software
field: data-engineering
product: kestra
tags: [webhook, http, secret-key, fetchtype, headers, trigger-body]
level: practitioner
status: docs-checked
description: "Start Kestra flows from HTTP requests with the Webhook trigger: URL format, secret key, reading body and headers, fetchType, waiting for outputs, and safety."
sources:
  - https://kestra.io/docs/workflow-components/triggers/webhook-trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Accepts `GET`, `POST` and `PUT` on:

```bash
https://{kestra_domain}/api/v1/main/executions/webhook/{namespace}/{flowId}/{key}
```

```yaml
triggers:
  - id: webhook
    type: io.kestra.plugin.core.trigger.Webhook
    key: "{{ secret('WEBHOOK_KEY') }}"
    when: "{{ trigger.headers['X-GitHub-Event'] contains 'push' }}"
```

Keep the `key` in Secrets, not in YAML.

- Body: `trigger.body`. `fetchType`: `FETCH` (default, in memory, binary base64-encoded), `STORE` (internal storage, URI on `trigger.uri`), `NONE`.
- `trigger.headers` maps names to lists of values, so use `contains`. Matching is case-sensitive.
- Multipart: files on `trigger.parts` (always stored internally), text on `trigger.formFields`.

Response: immediate by default. `wait: true` holds the connection until the execution finishes or times out. `returnOutputs: true` returns flow outputs as JSON (the flow needs at least one `outputs` entry). `responseContentType` sets only the header.

Security:

- Anyone with the URL can call it; treat request data as untrusted.
- In script tasks, pass request values through `env`, not `commands` or `script`, and never `render()` them.
- With `STORE`, `when` conditions on `trigger.body` will not work.

## Checked

2026-11-04. Confirmed against "Trigger Flows from External Apps via Secure Webhook URLs" (triggers/webhook-trigger): accepted methods and URL, key in Secrets, fetchType table, base64 for binary bodies, multipart parts and formFields, header list shape and case sensitivity, env versus render() security guidance, STORE and when limitation, wait, returnOutputs, responseContentType. No claims removed.
Method: documentation only; no commands were run.
