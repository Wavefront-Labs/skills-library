---
id: computing-software.cloud-infrastructure-engineering.aws.cognito-app-clients-and-auth-flows
name: cognito-app-clients-and-auth-flows
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cognito, auth-flows, srp-auth, initiate-auth, app-client-secret, token-validity]
level: practitioner
status: docs-checked
description: "Configure Cognito user pool app clients: public vs confidential clients, allowed auth flows (SRP, password, refresh, custom, choice-based), token validity and secret hashes."
sources: ["https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-refresh-token.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html#cognito-user-pools-computing-secret-hash", "https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/create-user-pool-client.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cognito app clients and auth flows

## 1. Public vs confidential clients
- **Public** (SPA, mobile): no client secret (it would be extractable). Use SRP or managed
  login with authorization code + PKCE.
- **Confidential** (server-side web app, backend): has a client secret; API calls must
  include `SECRET_HASH` = Base64(HMAC_SHA256(client_secret, username + client_id)).
```bash
aws cognito-idp create-user-pool-client --user-pool-id eu-west-1_ABC --client-name web-spa \
  --no-generate-secret \
  --explicit-auth-flows ALLOW_USER_SRP_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --prevent-user-existence-errors ENABLED \
  --enable-token-revocation \
  --access-token-validity 60 --id-token-validity 60 --refresh-token-validity 30 \
  --token-validity-units AccessToken=minutes,IdToken=minutes,RefreshToken=days
```

## 2. Auth flows (`ExplicitAuthFlows`)
| Flow | What it is | When |
|---|---|---|
| `ALLOW_USER_SRP_AUTH` | Secure Remote Password: password never sent | SDK/Amplify sign-in |
| `ALLOW_USER_PASSWORD_AUTH` | plain username/password over TLS to Cognito | migrations (user migration trigger needs it), legacy; avoid otherwise |
| `ALLOW_ADMIN_USER_PASSWORD_AUTH` | server-side `AdminInitiateAuth` with IAM creds | trusted backends |
| `ALLOW_CUSTOM_AUTH` | Lambda-driven challenges | custom OTP, magic links |
| `ALLOW_USER_AUTH` | choice-based auth: passkeys, email/SMS OTP, password | Essentials/Plus tiers' passwordless options |
| `ALLOW_REFRESH_TOKEN_AUTH` | `REFRESH_TOKEN_AUTH` refresh requests | almost always; not compatible with refresh token rotation (see section 5) |
Only enable what each client uses; every flow is attack surface.

## 3. Calling the API
```bash
aws cognito-idp initiate-auth --client-id <id> --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=alice,PASSWORD='***',SECRET_HASH=<hash>
```
Response is either `AuthenticationResult` (tokens) or a `ChallengeName`
(`SMS_MFA`, `SOFTWARE_TOKEN_MFA`, `NEW_PASSWORD_REQUIRED`, `PASSWORD_VERIFIER` for SRP,
`SELECT_CHALLENGE` for choice-based) answered via `respond-to-auth-challenge` with the
returned `Session`. Use Amplify/SDK helpers for SRP math.

## 4. OAuth settings (managed login / hosted UI)
For browser apps prefer managed login with `AllowedOAuthFlows=code`, PKCE,
`AllowedOAuthScopes=openid email profile`, exact `CallbackURLs`/`LogoutURLs` (HTTPS,
localhost allowed for dev). Implicit flow is legacy.

## 5. Token validity and revocation
- Access/ID tokens: 5 minutes to 1 day (default unit hours). Refresh: 60 minutes to 10 years
  (default unit days; a value of 0 is replaced by 30 days).
- Refresh token rotation (`RefreshTokenRotation` on the app client, optional grace period)
  issues a new refresh token on each refresh, but it is not compatible with
  `REFRESH_TOKEN_AUTH`: disable `ALLOW_REFRESH_TOKEN_AUTH` and refresh with
  `GetTokensFromRefreshToken`. The session still ends at the original refresh validity.
- Token revocation is on by default for new app clients created without the parameter
  (`--enable-token-revocation` / `--no-enable-token-revocation`); it lets `revoke-token`
  invalidate a refresh token and its access tokens (for Cognito-verified APIs;
  self-verified JWTs remain valid until expiry).
- `create-user-pool-client` sets any attribute you omit to its default; pass the full
  intended configuration.
- `GlobalSignOut`/`AdminUserGlobalSignOut` revokes all of a user's refresh tokens.

## Gotchas
- `NotAuthorizedException: Unable to verify secret hash` = client has a secret but the call
  omitted or miscomputed `SECRET_HASH`.
- `prevent-user-existence-errors` on avoids username enumeration via error differences.
- Read/write attribute permissions per client: restrict which attributes clients can update
  (e.g. not `custom:role`).

## Verify
- [ ] Each client enables only required flows; SPAs have no secret and use SRP or code+PKCE.
- [ ] Token lifetimes match policy; revocation works (revoked refresh token fails).
- [ ] Attribute write permissions exclude privileged attributes.

## Checked

Checked 2026-10-27 against the Amazon Cognito Developer Guide, the Cognito quotas page, the aws-cli cognito-idp reference and the botocore cognito-idp 2016-04-18 model.
- Confirmed: ExplicitAuthFlows values, challenge names, and the create-user-pool-client flags (`--no-generate-secret`, `--enable-token-revocation`, `--prevent-user-existence-errors`, `--token-validity-units`).
- Confirmed: access/ID token validity 5 minutes to 1 day; refresh token 60 minutes to 10 years, default 30 days, default units hours/hours/days; token revocation is on by default for new app clients.
- Corrected: refresh token rotation is not compatible with `REFRESH_TOKEN_AUTH` (use `GetTokensFromRefreshToken`); removed unsupported "default 1 h" and "pre-passwordless era" wording.
- Confirmed: SECRET_HASH requirement and the "Unable to verify secret hash" error text; HTTPS callback URLs with http://localhost allowed for testing.

Method: documentation only; no commands were run.
