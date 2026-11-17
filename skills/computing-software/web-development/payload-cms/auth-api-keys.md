---
id: computing-software.web-development.payload-cms.auth-api-keys
name: auth-api-keys
category: computing-software
field: web-development
product: payload-cms
tags: [api-keys, useapikey, service-account, integration-auth]
level: practitioner
status: docs-checked
description: "Enable per-user API keys with useAPIKey for non-expiring third-party integrations, and know the rules about display, secrets and revocation."
sources:
  - https://payloadcms.com/docs/authentication/api-keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API keys

Goal: let a third-party service authenticate as a specific Payload user.

```ts
export const ThirdPartyAccess: CollectionConfig = {
  slug: 'third-party-access',
  auth: { useAPIKey: true },
  fields: [],
}
```

Create a user that represents the integration, give it only the role it needs, then generate its key in the Admin Panel (available to users accepted by the admin collection's `access.admin`).

Rules from the docs:

- A generated key is shown only once; afterwards reads omit it and show only a masked preview ending in the last four characters.
- Built-in read operations do not return the key unless you explicitly reveal it (see the docs section on revealing API keys).
- The key is independent of the user's password: changing or resetting the password does not disable it. Regenerate or remove the key to end access.
- Keys are encrypted with `PAYLOAD_SECRET`; changing the secret invalidates them (see secret rotation).
- Restrict who can generate, regenerate and revoke by overriding the generated `apiKey` field's `create` and `update` access.

Send the key in the `Authorization` header as `<collection-slug> API-Key <key>`. `useAPIKey: { reveal: true }` exposes keys on reads; `disableLocalStrategy` can be set when the collection should authenticate by API key only.

## Checked

2026-11-04. Read authentication/api-keys in the payloadcms/payload docs. Confirmed: every rule listed (shown once, masked preview, independent of password, encrypted with PAYLOAD_SECRET, access on the apiKey field). Replaced: the verify step with the documented header format. Added: reveal option.
Method: documentation only; no commands were run.
