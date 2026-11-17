---
id: computing-software.cybersecurity-defensive.dex.dex-custom-claims-and-federated-claims
name: dex-custom-claims-and-federated-claims
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [claims, federated-claims, groups, id-token]
level: practitioner
status: docs-checked
description: "Know the non-standard claims Dex adds to ID tokens: groups, federated_claims, email, email_verified, name and preferred_username."
sources:
  - https://dexidp.io/docs/configuration/custom-scopes-claims-clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Beyond required OpenID Connect claims, Dex implements these non-standard claims:

- `groups`: list of strings, the groups the user belongs to.
- `federated_claims`: the connector id and the user id assigned at the provider.
- `email`: the user's email.
- `email_verified`: whether the upstream provider verified the email.
- `name`: the user's display name.
- `preferred_username`: shorthand name the user wants to be called.

The `federated_claims` claim looks like this:

```json
"federated_claims": {
  "connector_id": "github",
  "user_id": "110272483197731336751"
}
```

It appears when the `federated:id` scope is requested.

Gotchas:

- The `email`, `profile`, `groups` and `federated:id` scopes control whether these claims are included; see the supported scopes skill.

## Checked

2026-11-08: Read the Dex Scopes and Claims page in full. Confirmed the claim list and descriptions, the federated_claims format and the scopes that add claims. Removed insecureSkipEmailVerified, emailToLowercase and the login check, which that page does not state.
Method: documentation only; no commands were run.
