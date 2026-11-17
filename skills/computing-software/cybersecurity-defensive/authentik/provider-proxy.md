---
id: computing-software.cybersecurity-defensive.authentik.provider-proxy
name: provider-proxy
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, proxy-provider, forward-auth, outpost, unauthenticated-paths, headers]
level: advanced
status: docs-checked
description: "Reference for the authentik proxy provider: proxy and forward-auth modes, injected X-authentik headers, sign-out, unauthenticated paths, backend override and host header mappings."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: protect applications that do not speak OIDC, SAML or LDAP, using an authentik outpost.

## Modes
- **Proxy**: the outpost proxies to one upstream.
- **Forward auth (single application)**: your reverse proxy forwards and asks the outpost to authorize one app.
- **Forward auth (domain level)**: one provider protects many apps under a parent domain; it cannot enforce different per-application authorization, so use single-application mode when apps need their own policies or bindings.

## Headers sent upstream
`X-authentik-username`, `X-authentik-groups` (pipe separated), `X-authentik-entitlements`, `X-authentik-email`, `X-authentik-name`, `X-authentik-uid`, plus `X-authentik-meta-outpost`, `-provider`, `-app`, `-version`. In proxy mode `X-Forwarded-Host` keeps the client's original Host (the Host header is set to the upstream). Static extra headers: `additionalHeaders:` map in group or user attributes.

## Ports and logout
Outpost listens on `9000` (HTTP) and `9443` (HTTPS); with an HTTPS upstream and no forward auth, reach the outpost via HTTPS. Log out at `/outpost.goauthentik.io/sign_out` on the application host (proxy and single-app modes) or on the provider's auth URL host (domain level). It invalidates all of that user's sessions in the outpost.

## Unauthenticated paths
**Unauthenticated Paths** / **Unauthenticated URLs**: one Rust regex per line. Proxy and single-app modes match the request path; domain-level mode matches the full URL including scheme and host. An uncompilable pattern is skipped with a warning in the outpost logs, silently leaving that path protected.

## Scope mappings for dynamic behavior
Add under the provider's **Additional scopes**; evaluated only at login:
```python
return {"ak_proxy": {"backend_override": f"http://foo.bar.baz/{request.user.username}"}}
```
```python
return {"ak_proxy": {"host_header": "my-internal-host-header"}}
```
`host_header` needs 2025.6.1 or later. To use the provider's Internal host, parse `provider.proxyprovider.internal_host` with `urlparse` and return `parsed_url.netloc`.

Troubleshooting: search outpost or server logs for the provider's `client_id` (Authentication tab).

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/proxy/.
Nothing was removed.
Method: documentation only; no commands were run.
