---
id: computing-software.cybersecurity-defensive.authelia.privacy-policy-link-and-acceptance
name: privacy-policy-link-and-acceptance
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, privacy-policy, gdpr, user-acceptance, portal-ui, compliance]
level: intro
status: docs-checked
description: "Show a privacy policy link in the Authelia portal and optionally require per-browser acceptance, with the OpenID Connect implicit consent caveat."
sources:
  - https://www.authelia.com/configuration/miscellaneous/privacy-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Operators bound by the GDPR or similar laws can surface their policy in the Authelia portal.

```yaml
privacy_policy:
  enabled: true
  require_user_acceptance: false
  policy_url: 'https://www.example.com/privacy'
```

- `enabled` shows the privacy policy link in the interface.
- `policy_url` is the link target, your own privacy policy. It must be an absolute URL with the `https://` scheme and is required when `enabled` is true.
- `require_user_acceptance` shows a dialog drawer at the bottom of the page. Acceptance is recorded in the browser's `localStorage`, so it is per browser, and a user who has not accepted should not be able to interact with the Authelia UI by normal means.

A caveat from the documentation: OpenID Connect clients with `consent_mode: implicit` seldom bring up the Authelia UI when the user is already signed in, so the acceptance dialog may never be seen. The maintainers will not add a check for implicit mode, because that mode is unlikely to comply with those laws and is not strictly compliant with the specification either. The docs recommend that with `require_user_acceptance` enabled you avoid implicit consent mode, or accept the risk.

Acceptance is recorded and checked in the browser's `localStorage`, so it is per browser.

Check: open the portal in a private window and confirm the acceptance dialog appears.

## Checked

2026-11-08. Read the full Authelia Privacy Policy page. Confirmed the three options, the localStorage per-browser acceptance, the implicit consent mode caveat, and that policy_url must be an absolute https URL and is required when enabled. Removed the explicit and pre-configured consent advice and the audit-trail remark, which the page does not state.

Method: documentation only; no commands were run.
