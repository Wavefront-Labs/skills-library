---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-authentication-request-parameters
name: oidc-authentication-request-parameters
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-authentication-request-parameters, oidc-core-flows, prompt, max_age, login_hint, id_token_hint, acr_values, ui_locales, identity-protocols]
level: practitioner
status: docs-checked
description: "Use OIDC request parameters correctly: prompt, max_age, login_hint, id_token_hint, acr_values, display and ui_locales, with error codes returned."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication request parameters

Goal: control the login experience and assurance.

- `prompt`: space-delimited, case-sensitive list. `none` shows no UI and returns an error if the user is not already authenticated or consent is missing (typically `login_required` or `interaction_required`; also `consent_required`, `account_selection_required`); `login` asks for re-authentication; `consent` asks for consent; `select_account` asks the user to pick an account. If `none` appears with any other value, an error is returned.
- `max_age`: allowable seconds since the last active authentication; if exceeded the OP must attempt to re-authenticate, and the ID Token then includes `auth_time`. `max_age=0` is equivalent to `prompt=login`.
- `login_hint`: hint about the login identifier the user might use; `id_token_hint`: an ID Token previously issued by the OP as a hint about the user's current or past session; if that user is not logged in the OP returns an error such as `login_required`.
- `acr_values`: space-separated requested authentication context class values in order of preference, a voluntary request; for a mandatory one use the `claims` parameter with `essential`.
- `display` (`page`, `popup`, `touch`, `wap`), `ui_locales`, `claims_locales`.

Gotchas:
- Check the returned `acr` and `auth_time` yourself: the RP should check `acr` is appropriate and, if `auth_time` was requested, that not too much time has elapsed.
- The OP uses `login_hint` at its discretion.

Verify: send `prompt=none` with no OP session and expect an error redirect (typically `login_required`).

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 3.1.2.1, 3.1.2.6, 3.1.3.7 and 5.5.1. Removed: the claim that `login_hint` for a different user can confuse account switching.
Method: documentation only; no commands were run.
