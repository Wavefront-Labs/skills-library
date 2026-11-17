---
id: computing-software.cybersecurity-defensive.authentik.stage-password
name: stage-password
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, password-stage, backends, password-lockout, passwordless, skip-password]
level: practitioner
status: docs-checked
description: "Configure the authentik Password stage: backends, attempt limits, and conditionally skipping it for users with WebAuthn or Duo."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/password/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: verify the pending user's password against one or more backends.

## Options
- **Backends** (tested in order): User database + standard password, + app passwords, + LDAP password, + Kerberos password.
- **Failed attempts before cancel**: how many failed password submissions are allowed before the flow is canceled.
- **Allow show password**, **Configuration flow**.

Bind after Identification and before Authenticator Validation or User Login. If the Identification stage embeds the Password stage, do not bind it again.

## Dynamically skip the stage
Create an Expression Policy that returns True only when the Password stage should run, bind it to the Password **stage binding** (not the flow or the stage object), enable **Evaluate when stage is run** and disable **Evaluate when flow is planned**.
```python
from authentik.stages.authenticator_webauthn.models import WebAuthnDevice

pending_user = request.context.get("pending_user")
if not pending_user:
    return True

return not WebAuthnDevice.objects.filter(user=pending_user, confirmed=True).exists()
```
For Duo, import `DuoDevice` from `authentik.stages.authenticator_duo.models` the same way. No need for **Negate Result**. With several policies, `all` requires every one to pass. The built-in `default-authentication-flow` already has a policy `default-authentication-flow-password-stage` on this binding; when adding a second, set the binding's policy engine mode to `all`.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/password/.
Removed as not confirmed by that page: Enterprise lockout options, lock/unlock API and events.
Method: documentation only; no commands were run.
