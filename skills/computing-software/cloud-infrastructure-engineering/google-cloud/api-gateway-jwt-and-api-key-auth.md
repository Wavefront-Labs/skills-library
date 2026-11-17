---
id: computing-software.cloud-infrastructure-engineering.google-cloud.api-gateway-jwt-and-api-key-auth
name: api-gateway-jwt-and-api-key-auth
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, api-management, api-gateway-jwt, api-gateway-auth, api-keys, firebase-auth]
level: practitioner
status: docs-checked
description: "Secure API Gateway with securityDefinitions: API keys restricted to the managed service, JWT validation for Firebase, Auth0, Google ID tokens, and reading the forwarded user info."
sources: ["https://cloud.google.com/api-gateway/docs/authenticate-api-keys", "https://cloud.google.com/api-gateway/docs/authenticating-users-jwt", "https://cloud.google.com/api-gateway/docs/authentication-method"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway JWT and API key auth

## 1. API keys
```yaml
securityDefinitions:
  api_key: {type: apiKey, name: key, in: query}     # or in: header, name: x-api-key
security: [{api_key: []}]
```
After deploying, enable the API's **managed service** in the consumer project and create a key restricted to it:
```bash
gcloud services enable $(gcloud api-gateway apis describe orders-api --format='value(managedService)')
gcloud services api-keys create --display-name=partner-x \
  --api-target=service=$(gcloud api-gateway apis describe orders-api --format='value(managedService)')
```
API keys identify the calling project (quotas, analytics), not a user: never the only control for sensitive data.

## 2. JWT
```yaml
securityDefinitions:
  firebase:
    authorizationUrl: ""
    flow: implicit
    type: oauth2
    x-google-issuer: https://securetoken.google.com/<FIREBASE_PROJECT>
    x-google-jwks_uri: https://www.googleapis.com/service_accounts/v1/metadata/x509/securetoken@system.gserviceaccount.com
    x-google-audiences: <FIREBASE_PROJECT>
paths:
  /orders:
    get:
      security: [{firebase: []}]
```
`x-google-jwks_uri` (OpenAPI 2.0) or `jwksUri` (3.x) is required. `x-google-audiences` is optional: API Gateway accepts any JWT whose `aud` is `https://<SERVICE_NAME>`; list extra client IDs there (comma-separated in OpenAPI 2.0, a list in 3.x). Each security definition must have a different issuer. API Gateway caches the JWKS for five minutes. The token claims `iss`, `sub`, `aud`, `iat` and `exp` must be present.

## 3. In the backend
The gateway validates the token and sends the JWT payload, base64url-encoded, in `X-Apigateway-Api-Userinfo`.
When the backend address comes from `x-google-backend`, the gateway overrides the original `Authorization` header, so read the userinfo header instead. Authorise on claims in the backend.

## Gotchas
- A `security` section at API level applies to the whole API; method-level settings override it.
- Key restrictions (application and API restrictions) are separate settings on the key; use API restrictions on production keys.
- Clients send the token as `Authorization: Bearer <token>`, or in the `access_token` query parameter if headers are not possible.

## Verify
- [ ] Calls without a token or key are rejected; a valid token succeeds and the backend receives `X-Apigateway-Api-Userinfo`.

## Checked
2026-10-27. Confirmed against the API Gateway Using JWT to authenticate users page (required claims, audiences default and optionality, jwks_uri required, five-minute JWKS cache, one issuer per definition, method-level override, X-Apigateway-Api-Userinfo, Authorization override, access_token query parameter), Use API Keys page (managed service enable, API restrictions, key identifies the project) and gcloud services api-keys create flags. Removed: the Auth0/Okta and Google ID token issuer details, X-Forwarded-Authorization (documented for ESPv2 only), the exact 401 message, and the security: [] public-endpoint tip. Corrected: x-google-audiences is optional.
Method: documentation only; no commands were run.
