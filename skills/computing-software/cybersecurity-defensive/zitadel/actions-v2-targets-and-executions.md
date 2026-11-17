---
id: computing-software.cybersecurity-defensive.zitadel.actions-v2-targets-and-executions
name: actions-v2-targets-and-executions
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, actions, webhooks, targets, executions, extensibility]
level: advanced
status: docs-checked
description: "Extend ZITADEL with Actions v2 by pointing executions at external HTTP targets for requests, responses, functions and events."
sources:
  - https://zitadel.com/docs/concepts/features/actions_v2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Actions v2 modify ZITADEL's behavior at specific API calls, events or functions, for business rules ZITADEL cannot anticipate. Examples from the documentation: domain-specific validation before a user is created or authenticated, assigning roles from ADFS 2016+ groups, storing user metadata for applications, and restricting registration to certain email domains.

Three components:

- Endpoint: external logic that can receive an HTTP POST request.
- Target: a ZITADEL resource describing how to trigger an endpoint.
- Execution: a ZITADEL resource saying when to trigger which targets.

Execution conditions:

- Request: react to or change requests to ZITADEL, for example adding information to new users.
- Response: react to or change responses, for example provisioning new users into other systems.
- Function: replace the behavior of earlier Actions.
- Event: react to ZITADEL events, for example notify someone when a user gets locked.

Defined Actions v2 run in addition to the older Actions. A migration guide exists for moving from v1. The documentation also provides test examples for requests, request manipulation, request signature checks, responses and events.

Build the endpoint first, test it with a webhook inspection site, then create the target and execution. Verify request signatures in your endpoint.

## Checked
2026-11-08. Confirmed against the ZITADEL Actions v2 concept page: use cases, endpoint, target and execution components, request, response, function and event conditions, running in addition to v1 actions, migration guide, example list. The webhook inspection and signature-check advice is general practice, not a documented figure.
Method: documentation only; no commands were run.
