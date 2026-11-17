---
id: computing-software.cybersecurity-defensive.authentik.expression-policies
name: expression-policies
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, expression-policy, python, pending-user, flow-plan, auth-method]
level: advanced
status: docs-checked
description: "Write authentik expression policies safely: pending_user vs request.user, prompt_data, flow_plan context, and auth_method values and auth_method_args shapes."
sources:
  - https://docs.goauthentik.io/customize/policies/types/expression/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: custom server-side Python policies. Creating or editing them is a highly privileged permission since the code runs inside authentik.

Return True to pass. Example: run an MFA stage only for one user when bound to the stage binding:
```python
if request.context["pending_user"].username == "marie":
    return True
return False
```

## Pitfalls
- In flows `request.user` can still be AnonymousUser or the previous user until a login or user-write stage runs. Use `pending_user = request.context.get("pending_user")`.
- Prompt answers are in `context["prompt_data"]`, e.g. `email = context["prompt_data"]["email"]`.
- Read or change flow state through `context["flow_plan"]` and `context["flow_plan"].context`; this can alter the rest of the flow. Some keys such as `prompt_data` are mirrored into the root policy context, but not every flow-plan key is.

## auth_method
Values include `password`, `auth_mfa` (MFA without a password step), `auth_webauthn_pwl` (passkey passwordless), `token` (for example an app password), `jwt` (M2M external JWT), `ldap`. `context["auth_method_args"]` shape depends on it:
- `auth_mfa`: `{"mfa_devices": [{"pk": 1, "app": "otp_static", "name": "Static Token", "model_name": "staticdevice"}]}`
- `token`: either `{"token": {"pk": ..., "app": "authentik_core", "name": ..., "model_name": "token"}}` or `{"identifier": "service-account-token"}`
- `ldap`: `{"source": {}}`

Related sample pages cover source switching, flow context keys, unique email, unique username regardless of case, and allowed email domains.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/customize/policies/types/expression/ (read in full).
