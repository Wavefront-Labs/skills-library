---
id: computing-software.cybersecurity-defensive.authentik.stage-authenticator-validate
name: stage-authenticator-validate
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, authenticator-validation, mfa, webauthn, throttling, device-classes]
level: advanced
status: docs-checked
description: "Configure the authentik Authenticator Validation stage: not-configured action, device classes, multiple MFA methods, validation threshold, WebAuthn hints and throttling."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_validate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: require an already enrolled authenticator (Duo, Email, SMS, Static, TOTP, WebAuthn) during login. Place it after Identification and Password, before User Login.

## Options
- **Not configured action**: **Skip** (continue without MFA), **Deny**, or **Configure** (inject one of the **Configuration stages** and continue when it succeeds).
- **Device Classes**: which authenticator types are usable.
- **Last validation threshold**: skip if a compatible device validated within the window. For TOTP, Static and SMS, values under `seconds=30` are useless.
- **WebAuthn User verification**, **WebAuthn Hints**, **WebAuthn Device type restrictions**.
- Throttling factors per class: Email, SMS, TOTP, Static.

## Require several methods
Add one validation stage per method, each with a different **Device Classes** value, **Not configured action** = Configure and its own setup stage (for example `totp` with the TOTP setup stage, `webauthn` with the WebAuthn setup stage); bind both in order. To require at least two enrolled methods of any type, use an expression policy counting classes:
```python
from authentik.stages.authenticator import devices_for_user

pending_user = request.context.get("pending_user")
if not pending_user or not pending_user.pk:
    return False

device_types = {
    device.__class__.__name__.lower().replace("device", "")
    for device in devices_for_user(pending_user, confirmed=True)
}

return len(device_types) >= 2
```
Selecting multiple configuration stages on one validation stage lets the user choose.

## Passwordless
Currently WebAuthn only. Build an Authentication flow with an Authenticator Validation stage allowing `WebAuthn`, any extra verification, then a User Login stage. Users reach it directly or via the Identification stage's **Passwordless flow** link. Success is logged as `auth_method` `auth_webauthn_pwl`. Firefox has known issues with some Touch ID/platform authenticator flows.

## Hints and restrictions
Hints (Security key, Client device, Hybrid; order matters) are advisory and browsers may ignore them. Device type restrictions are an allowlist from FIDO Alliance MDS data; they only match devices enrolled in 2024.4 or later that returned a known AAGUID, so older enrolments need re-enrolling.

## Throttling
Delay between attempts is `factor * 2^(n - 1)` seconds (default factor 1 gives 1, 2, 4, 8...). A success resets it; factor 0 disables it. WebAuthn and Duo are not throttled. After a success, the last-used authenticator is preferred next time.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_validate/.
Nothing was removed.
Method: documentation only; no commands were run.
