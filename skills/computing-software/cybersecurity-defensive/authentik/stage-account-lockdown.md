---
id: computing-software.cybersecurity-defensive.authentik.stage-account-lockdown
name: stage-account-lockdown
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, account-lockdown, incident-response, revoke-tokens, deactivate-user]
level: advanced
status: docs-checked
description: "Configure the authentik Account Lockdown stage (Enterprise, 2026.5): deactivate user, unusable password, delete sessions, revoke tokens, completion flow and events."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/account_lockdown/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: execute destructive security actions on a target account. Include warnings and confirmation steps in the flow before this stage.

## Settings (all enabled by default except completion flow)
- **Deactivate user** (`is_active` False)
- **Set unusable password** (local password only; external source passwords unchanged)
- **Delete sessions** (not recommended to disable, an attacker's active session would continue)
- **Revoke tokens** (API, app password, recovery, verification, OAuth tokens and grants)
- **Completion flow** (must have Authentication set to **No authentication required**)

## Target and reason
The API pre-plans the flow with the chosen user as `pending_user`; the target must be a real user, not the anonymous user or an internal service account, else the stage fails with "No target user specified". The reason comes from `prompt_data.lockdown_reason`, then `lockdown_reason` in plan context, else empty.

## Self-service
If the target is the logged-in user and **Delete sessions** is on, the session dies, so the stage redirects to the Completion flow. With it off, the flow continues normally.

## Event
A **User Write** event is created with context `action_id` `account_lockdown`, `reason` and `affected_user`. For notification rules match action `user_write` and query `context.action_id = "account_lockdown"`.

## Example policy: completion stage only for admin-triggered lockdowns
```python
target_user = request.context.get("pending_user")
current_user = request.http_request.user

return bool(target_user and current_user and target_user.pk != current_user.pk)
```
A Prompt field with **Initial value expression** can show a dynamic warning using `user` and `http_request` (escape usernames with `django.utils.html.escape`).

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/account_lockdown/.
Nothing was removed.
Method: documentation only; no commands were run.
