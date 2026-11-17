---
id: computing-software.cybersecurity-defensive.authentik.stage-deny
name: stage-deny
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, deny-stage, block-ip-range, inactive-users, recovery-flow]
level: practitioner
status: docs-checked
description: "Use the authentik Deny stage to stop a flow, block an IP range, or stop password recovery for inactive users, including the account state disclosure tradeoff."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/deny/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: end a flow immediately with access denied when a bound policy passes. The stage has no settings of its own.

Required: disable **Evaluate when flow is planned** on its stage binding. Otherwise denial can happen during planning, before the checks that were meant to decide it.

## Block an IP range
Create a Deny stage, an expression policy and bind the policy to the Deny stage binding:
```python
from ipaddress import ip_network

return ak_client_ip in ip_network("203.0.113.0/24")
```
When the policy passes, the Deny stage runs and the flow stops.

## Block recovery for inactive users
Deactivation prevents login but not recovery emails or password changes.
1. Add a Deny stage to the recovery flow after Identification and before the Email stage.
2. Policy:
```python
pending_user = request.context.get("pending_user")

return bool(
    pending_user
    and pending_user.pk
    and not pending_user.is_active
)
```
3. Bind to the Deny stage binding; disable **Evaluate when flow is planned**, enable **Evaluate when stage is run**, since `pending_user` only exists after Identification.

Active users and placeholder users (unknown identifiers) skip the Deny stage.

Warning: the denial differs from the **Email sent.** challenge shown for unknown and active accounts, so an attacker can learn that an account exists or is inactive. A Deny stage cannot both stop recovery and keep the response indistinguishable; use only if that disclosure is acceptable.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/deny/.
Removed as not confirmed by that page: deny_message context key.
Method: documentation only; no commands were run.
