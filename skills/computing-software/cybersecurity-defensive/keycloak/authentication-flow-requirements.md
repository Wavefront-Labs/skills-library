---
id: computing-software.cybersecurity-defensive.keycloak.authentication-flow-requirements
name: authentication-flow-requirements
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, authentication-flow, execution-requirement, conditional, subflow]
level: practitioner
status: docs-checked
description: "Build or modify Keycloak authentication flows correctly using Required, Alternative, Conditional and Disabled executions and sub-flows."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/flows.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authentication flow requirements
You cannot modify the built-in flows, only alter their requirements. To customise, copy one: in *Authentication* use the row action list (three dots) > *Duplicate* and name the new flow, edit it, then use *Bind flow* to bind it (for example as the Browser flow).

Top-level flow type: `basic` for everything except authenticating clients; `client` only for client authentication. Sub-flow type is `basic` (default) or `form`.

Requirements per execution:
- **Required**: all required elements run sequentially; the flow terminates if one fails.
- **Alternative**: only one element must succeed. Alternatives in a flow that also contains Required elements do not execute, because the Required elements are sufficient.
- **Conditional** (sub-flows): the sub-flow's executions must evaluate to logical statements. If all are true it acts as Required; if any is false, or if it has no condition execution, it acts as Disabled.
- **Disabled**: skipped.

Default browser flow: *Cookie* (alternative) succeeds when an SSO cookie exists and nothing else runs; otherwise the alternative *forms* sub-flow runs *Username Password Form* (required) then *Browser - Conditional 2FA*, which executes depending on *Condition - User Configured* and *Condition - credential*, then *OTP Form*. *WebAuthn Authenticator* and *Recovery Authentication Code Form* are inside that sub-flow, Disabled by default; set them to Alternative to offer them.

Warning from the docs: test your flow configuration for security holes, including corner cases such as removing credentials from a test user's account.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/flows.adoc. Removed (not on the page): the lock-out and second-admin-session gotcha, the "alternatives and required should not be mixed" paraphrase, the list of built-in flow names, and the Verify step.
Method: documentation only; no commands were run.
