---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-built-in-authentication-easy-auth
name: app-service-built-in-authentication-easy-auth
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, easy-auth, app-service-authentication, authsettingsv2, entra-id, token-store]
level: practitioner
status: docs-checked
description: "Configure App Service/Functions built-in authentication (Easy Auth) with Entra ID: authsettingsV2, unauthenticated action, allowed audiences, token store and reading user claims."
sources: ["https://learn.microsoft.com/azure/app-service/overview-authentication-authorization", "https://learn.microsoft.com/azure/app-service/configure-authentication-provider-aad", "https://learn.microsoft.com/azure/app-service/configure-authentication-user-identities", "https://learn.microsoft.com/azure/app-service/configure-authentication-file-based"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service built-in authentication (Easy Auth)

**Goal:** an App Service or Function requires Entra sign-in (or a valid bearer token) without
auth code in the app, and the app reads who the user is from headers.

## Enable with Entra
```bash
az webapp auth microsoft update -g rg -n app-orders \
  --client-id <app-registration-client-id> --issuer https://login.microsoftonline.com/<tenant>/v2.0 \
  --allowed-audiences api://<client-id> --client-secret-setting-name MICROSOFT_PROVIDER_AUTHENTICATION_SECRET
az webapp auth update -g rg -n app-orders --enabled true --action RedirectToLoginPage --enable-token-store true
```
Portal *Add identity provider* can create the app registration automatically (redirect URI
`https://<app>/.auth/login/aad/callback`). Prefer a **federated credential with the app's managed identity**
instead of a client secret (`--client-secret-setting-name OVERRIDE_USE_MI_FIC_ASSERTION_CLIENTID` pattern) to avoid secret expiry.

## Unauthenticated requests
| Setting | Use for |
|---|---|
| `RedirectToLoginPage` | Browser apps |
| `Return401` / `Return403` | APIs |
| `AllowAnonymous` | App decides per route (reads headers) |
Exclude paths (health probes, webhooks) with `globalValidation.excludedPaths` in authsettingsV2:
```bash
az webapp auth update -g rg -n app-orders --excluded-paths "[\"/health\",\"/api/webhooks\"]"
```

## Reading identity in code
Headers injected by the middleware: `X-MS-CLIENT-PRINCIPAL-NAME`, `X-MS-CLIENT-PRINCIPAL-ID`,
`X-MS-CLIENT-PRINCIPAL` (base64 JSON of claims). With token store: `X-MS-TOKEN-AAD-ACCESS-TOKEN`,
or the `/.auth/me` endpoint. Refresh: see the token store article for `/.auth/refresh`.
Restrict who may sign in with the authorization policy (`allowedPrincipals`), an app role check in code, or *Assignment required* on the enterprise app.

## APIs called by other services
Callers acquire a token for the app's audience (for example `api://<client-id>/.default`); set `allowedApplications` / `allowedPrincipals`
in `validation.defaultAuthorizationPolicy` to restrict which client apps/identities are accepted.

## Gotchas
- Don't trust the `X-MS-CLIENT-PRINCIPAL*` headers in code that may also run outside App Service's authentication middleware.
- Slots: auth configuration is per slot; register a redirect URI for each slot host name.
- Front Door/App Gateway in front: set `forwardProxy` (`NoProxy`, `Standard` or `Custom`; `Standard` honours `X-Forwarded-Host` from Front Door) so redirects use the public host name. It can't be set in the portal.

## Verify
- [ ] Anonymous `curl -i https://app-orders.azurewebsites.net/api/orders` returns 401 (API) or 302 to login (web).
- [ ] `/.auth/me` after sign-in returns the user's claims.
- [ ] `/health` stays anonymous for probes.

## Checked
2026-10-27. Confirmed on Microsoft Learn: configure-authentication-provider-aad (redirect URI `/.auth/login/aad/callback`, OVERRIDE_USE_MI_FIC_ASSERTION_CLIENTID),
configure-authentication-file-based (globalValidation.excludedPaths, forwardProxy NoProxy/Standard/Custom, defaultAuthorizationPolicy allowedApplications/allowedPrincipals),
overview-authentication-authorization (forwardProxy Standard and X-Forwarded-Host, not settable in portal), user-identities (X-MS-CLIENT-PRINCIPAL-* and X-MS-TOKEN-AAD-* headers),
CLI reference for `az webapp auth` (--action Return401/Return403/AllowAnonymous/RedirectToLoginPage, --excluded-paths, --enable-token-store) and `az webapp auth microsoft update`
(--client-id, --issuer, --allowed-audiences, --client-secret-setting-name).
Removed: `offline_access` refresh requirement, header-limit and spoofing statements, the unverified `allowedGroups` setting.

Method: documentation only; no commands were run.
