---
id: computing-software.systems-network-administration.immich.oauth-mobile-redirect
name: oauth-mobile-redirect
category: computing-software
field: systems-network-administration
product: immich
tags: [mobile-redirect, auto-launch, oauth-callback, custom-scheme, google]
level: practitioner
status: docs-checked
description: "Make OAuth work in the Immich mobile app when the provider rejects the custom scheme redirect, using the mobile-redirect route, plus auto launch behaviour."
sources:
  - https://docs.immich.app/administration/oauth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: log in with OAuth from the iOS or Android app when your provider will not accept `app.immich:///oauth-callback`, which is a custom URL scheme.

Some providers do not accept a custom scheme as a redirect URI. The docs give this workaround:

1. Have an http(s) endpoint forward requests to `app.immich:///oauth-callback`. Immich already provides one: `/api/oauth/mobile-redirect`.
2. Whitelist that endpoint as a valid redirect URI at the provider.
3. In Immich, Administration, Settings, OAuth, enable "Mobile Redirect URI Override" and enter the URL.

The Google example uses:

```
https://example.immich.app/api/oauth/mobile-redirect
```

and sets Mobile Redirect URI Override to Enabled (required). In the docs' Authentik, Authelia and Keycloak examples the override is left disabled.

Auto Launch makes the login page skip straight to the provider. To reach the normal login screen again use the browser back button or navigate to the login page directly. You can also request it per visit with:

```
/auth/login?autoLaunch=1
```

The docs suggest this when Immich is called from another app such as Nextcloud (External sites app plus the oidc app), so users land in a logged-in Immich.

Web login still needs `https://your-domain/auth/login` and `/user-settings` in the provider's redirect list.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/oauth (Auto Launch, Mobile Redirect URI, Google/Authentik/Authelia/Keycloak examples).
Removed or reworded: the claim that Google refuses custom schemes and the stated reason for disabled overrides.
Method: documentation only; no commands were run.
