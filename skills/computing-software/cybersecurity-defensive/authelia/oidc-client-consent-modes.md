---
id: computing-software.cybersecurity-defensive.authelia.oidc-client-consent-modes
name: oidc-client-consent-modes
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, consent, consent-mode, pre-configured-consent, implicit, gdpr]
level: practitioner
status: docs-checked
description: "Choose an Authelia OIDC client consent mode, set the remembered-consent duration, and weigh the privacy-policy interaction."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/clients/
  - https://www.authelia.com/configuration/miscellaneous/privacy-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each client has a `consent_mode`:

```yaml
clients:
  - client_id: '<CLIENT_ID>'
    consent_mode: 'pre-configured'
    pre_configured_consent_duration: '1 month'
```

| Value | Behaviour |
| --- | --- |
| `auto` | Default. `explicit` unless a pre-configured duration is set, then `pre-configured`. |
| `explicit` | Asks for consent on every authorization. |
| `implicit` | Assumes consent and never asks. |
| `pre-configured` | The user may remember consent for the configured duration. |

Details:

- If explicit consent is required by some condition, the fallback mode has no effect.
- `implicit` is not part of the specification and is discouraged. It is risky with public clients or an exposed client secret.
- Setting `pre_configured_consent_duration` without a mode enables `pre-configured`. The remembered consent is valid only when the subject and client ID are identical and the requested scopes and audience match the granted ones exactly.
- A matching `deny` rule in an authorization policy returns `access_denied` without asking for consent.

For privacy law compliance, the privacy policy option `require_user_acceptance` shows a dialog to users, but `implicit` clients will often not display the Authelia UI at all for an already signed-in user, so the dialog never appears. The documentation says to avoid `implicit` in that case.

Check: sign in twice with `pre-configured` mode and confirm the second login skips the consent screen until the duration ends.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Clients configuration page (consent_mode values and auto behaviour, implicit warning, pre_configured_consent_duration default and matching rules), the Provider page (deny rule and access_denied) and the Privacy Policy page (require_user_acceptance and the implicit mode caveat). Removed: nothing.

Method: documentation only; no commands were run.
