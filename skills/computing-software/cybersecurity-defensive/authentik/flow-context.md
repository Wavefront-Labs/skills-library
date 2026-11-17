---
id: computing-software.cybersecurity-defensive.authentik.flow-context
name: flow-context
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, flow-context, pending-user, prompt-data, reserved-keys, plan-context]
level: practitioner
status: docs-checked
description: "Reference for the authentik flow context: pending_user, prompt_data, redirect, auth_method and stage keys such as groups, user_path."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/context/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: know which context keys stages and policies read and write during a flow execution. Each execution has its own independent context.

Keys prefixed `goauthentik.io` are internal, may change without notice, and should not normally be modified in policies.

## Common keys
- `pending_user`: the user executing the flow. Not set automatically; the Identification stage sets it. Password and Authenticator validation stages use it, falling back to the request user.
- `prompt_data`: every Prompt stage field value, keyed by its Field Key (a field `email` submitted as `foo@bar.baz` gives `{"prompt_data": {"email": "foo@bar.baz"}}`). User Write can store these on `pending_user`.
- `redirect`: final URL after success.
- `pending_user_identifier`: set when Identification's *Show matched user* is disabled.
- `application`, `source`, `outpost` (dict with `"instance"` when an outpost runs the flow).

## Scenario keys
`is_sso` (true for source or application-authorize flows), `is_restored` (token object when resumed from an Email stage link or Source stage), `is_redirected` (reached via Redirect stage in Flow mode).

## Stage keys
- Consent: `consent_header`, `consent_permissions` (not for SAML).
- Deny: `deny_message` overrides the stage message.
- User write: `groups` (list of Group objects, not names), `user_path`, `user_type` (`internal`, `external` or `service_account`).
- Password: `user_backend`, `auth_method` (`password`, `token`, `ldap`, `auth_mfa`, `auth_webauthn_pwl`, `jwt`, `mtls`), `auth_method_args`.
- Email: `email_sent`, `email` (override recipient, default is the pending user's email).
- Invitation: `invitation`, `invitation_in_effect`, `token`.
- Redirect: `redirect_stage_target`; use `ak-flow://{slug}` for Flow mode, anything else is Static mode.
- Mutual TLS: `certificate` with serial_number, subject, issuer, fingerprints and `san`.

Example reading the first certificate email in an expression policy:
```python
emails = context["flow_plan"].context["certificate"]["san"].get("RFC822Name", [])
return emails[0] if emails else None
```

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
