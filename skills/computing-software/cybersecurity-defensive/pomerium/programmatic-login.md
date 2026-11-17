---
id: computing-software.cybersecurity-defensive.pomerium.programmatic-login
name: programmatic-login
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [programmatic-access, login-api, pomerium-redirect-uri, callback-handler, redirect-domain-whitelist]
level: practitioner
status: docs-checked
description: "Let a script obtain a Pomerium session token through the browser-based login API and callback, then call upstreams with it."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/programmatic-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scripts can log in like `gcloud`: request a signed login URL, have the user sign in via browser, and receive a token at a local callback.

1. Request a URL from any proxied service:

```
curl "https://$ANY_POMERIUM_PROXIED_SERVICE/.pomerium/api/v1/login?pomerium_redirect_uri=$MY_LOCAL_DEV_SERVICE"
```

The result is a sign-in URL on the authenticate service with `pomerium_redirect_uri`, `sig` and `ts` parameters.
2. The user opens it; the browser is redirected to your URI with a `pomerium_jwt` query parameter.
3. Your callback handler (you must run one) stores `pomerium_jwt` securely.
4. Call upstreams with `Authorization: Pomerium ${pomerium_jwt}` (also accepted: `Authorization: Bearer Pomerium-${pomerium_jwt}` and `X-Pomerium-Authorization: ${pomerium_jwt}`).

Caveats:
- By default only `localhost` redirect URIs are allowed; change with `programmatic_redirect_domain_whitelist`.
- `pomerium_jwt` is opaque; do not inspect or rely on its contents.
- Expect the underlying refresh token to stop working when the user changes password, access is revoked, or an admin removes, rotates or deletes the OAuth Client ID.

Alternative for local dev: route an endpoint to a bastion host and forward a port, e.g. `ssh -N -R 5001:localhost:8000 my-user@my-bastion-host.example.com`.

## Checked

2026-11-04. Confirmed against the Programmatic access page: login API path and pomerium_redirect_uri, sig and ts parameters, pomerium_jwt callback, localhost default and programmatic_redirect_domain_whitelist, opaque token note, refresh token expiry causes, header formats, bastion ssh -R alternative. Nothing removed.

Method: documentation only; no commands were run.
