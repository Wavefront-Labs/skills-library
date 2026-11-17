---
id: computing-software.cloud-infrastructure-engineering.google-cloud.programmatic-access-to-iap-with-oidc-tokens
name: programmatic-access-to-iap-with-oidc-tokens
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-aware-proxy, iap-programmatic-access, iap-oidc-token, id-token, service-account-auth, iap-client-id]
level: practitioner
status: docs-checked
description: "Call IAP-protected apps from scripts and services: mint an OIDC ID token with the IAP OAuth client ID or custom audience, for service accounts and users, and debug 401s."
sources: ["https://cloud.google.com/iap/docs/authentication-howto", "https://cloud.google.com/iap/docs/sharing-oauth-clients", "https://cloud.google.com/docs/authentication/get-id-token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Programmatic access to IAP with OIDC tokens

IAP accepts `Authorization: Bearer <ID token>` (or `Proxy-Authorization` if the app uses its own
Authorization header). The token's `aud` must be the IAP **OAuth client ID** of the resource, or a
configured programmatic/custom audience.

## Find the audience
```bash
gcloud iap settings get --project=<P> --resource-type=backend-services --service=<BACKEND>
# the OAuth client ID is also shown in the IAP page of the console for the resource
```

## Service account (most common)
```bash
# from a VM/Cloud Run with attached SA: metadata server
# from a VM/Cloud Run with an attached SA, fetch an ID token from the metadata server (see the get-id-token guide)
# from a workstation impersonating
TOKEN=$(gcloud auth print-identity-token --impersonate-service-account=caller@<P>.iam.gserviceaccount.com \
  --audiences=<CLIENT_ID>.apps.googleusercontent.com --include-email)
curl -H "Authorization: Bearer $TOKEN" https://app.example.com/api/health
```
Grant the SA `roles/iap.httpsResourceAccessor` on the backend (and pass any access levels).
Python: `google.oauth2.id_token.fetch_id_token(Request(), audience)`.

## Users (desktop flow)
Follow the *Programmatic authentication* guide's user-account sample: it obtains an ID token for the IAP OAuth client ID.

## Gotchas
- Google lists these credential types as accepted: an OAuth 2.0 ID token whose audience is the IAP application's client ID, an access token that includes the `openid` and `https://www.googleapis.com/auth/userinfo.email` scopes, or a self-signed or Google-issued JWT for a service account.
- For a wrong audience or a missing role, compare the token's `aud` with the client ID and check `roles/iap.httpsResourceAccessor` on the resource.

## Verify
- [ ] `curl` with the token returns the app response (200), and backend sees `x-goog-authenticated-user-email`.

## Checked

- Date: 2026-10-27
- Confirmed against the IAP *Programmatic authentication* guide (accepted credential types, `Authorization` or `Proxy-Authorization` header, ID token audience is the IAP client ID, access token must carry openid and email scopes), the roles reference (`roles/iap.httpsResourceAccessor`) and the gcloud references for `auth print-identity-token` (`--audiences`, `--include-email`) and `iap settings get` (`--resource-type`, `--service`).
- Fixed: the skill said access tokens are not accepted; the guide lists them as accepted when they carry the openid and email scopes. Removed: the metadata `format=full` URL, `programmaticClients` settings, the error-response table and the "IAP requires the email claim" note.

Method: documentation only; no commands were run.
