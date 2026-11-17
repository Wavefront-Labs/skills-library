---
id: computing-software.cloud-infrastructure-engineering.aws.cognito-user-and-identity-pools
name: cognito-user-and-identity-pools
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cognito, user-pool, identity-pool, authentication, oidc, oauth2, jwt, hosted-ui, managed-login, app-client, lambda-triggers, pre-token-generation, mfa, federation, saml, social-login, api-gateway-authorizer, refresh-token, srp, role-mapping, enhanced-flow, unauthenticated-identities]
level: practitioner
status: docs-checked
description: "Set up Cognito user pools (sign-in, MFA, managed login, federation, Lambda triggers, JWT verification) and identity pools (temporary AWS credentials for app users)."
sources: ["https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-multi-region.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-working-with-lambda-triggers.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html", "https://docs.aws.amazon.com/cognito/latest/developerguide/iam-roles.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cognito — user pools for *who are you*, identity pools for *what AWS can you touch*

**Goal:** an app whose users sign in (password, MFA, Google/SAML), receive JWTs your
API verifies correctly, and — only if needed — get scoped temporary AWS credentials.

## 1. Two different products
| | User pool | Identity pool (federated identities) |
|---|---|---|
| Does | Authenticates users, issues **ID / access / refresh** JWTs, hosts sign-in UI, federates to IdPs | Exchanges a token (Cognito user pool, Google, SAML, OIDC, or unauthenticated guest) for **STS credentials** via a role |
| Use when | Your API checks a JWT (API Gateway, ALB, AppSync, own code) | The app itself calls AWS (S3 upload, DynamoDB) directly |
Most apps need only a user pool. Add an identity pool only when the client must sign AWS calls.

## 2. User pool setup
- **Sign-in options**: username / email / phone; choose at creation — cannot change later.
  Mark email as a required, auto-verified attribute; set case-insensitive usernames.
- **App client**: one per client type. Browser/mobile = public client with **no secret**
  and SRP (`ALLOW_USER_SRP_AUTH`) + refresh (`ALLOW_REFRESH_TOKEN_AUTH`); backends = confidential
  client with secret and `ALLOW_ADMIN_USER_PASSWORD_AUTH` or client credentials.
  Disable `ALLOW_USER_PASSWORD_AUTH` unless you really send plaintext passwords.
- Token lifetimes: access/ID 5 min–1 day, refresh 60 min–10 years (default 30 days).
  Keep **token revocation** on (the default for new app clients) so sign-out invalidates refresh tokens.
- **MFA**: `OPTIONAL` with TOTP; SMS needs an origination identity and a way out of the SMS
  sandbox; email OTP needs the Essentials or Plus feature plan; `REQUIRED` for admin pools. Add
  **threat protection** (Plus plan) for adaptive MFA and compromised-credential checks.
- Password policy, account recovery (email before phone), and **user existence errors
  prevented** (`PreventUserExistenceErrors=ENABLED`) so sign-in does not leak which usernames exist.
- **Hosted UI / managed login** at `https://<domain>.auth.<region>.amazoncognito.com` or a
  custom domain (ACM cert in `us-east-1`); OAuth2 authorization-code grant with PKCE for SPAs
  — never implicit grant.

## 3. Federation
- Social IdPs (Google, Apple, Facebook, Amazon), **SAML 2.0** (Entra ID, Okta) and generic
  **OIDC**; map IdP claims → pool attributes. Federated users are created in the pool and
  receive the same JWTs as native users.
- Pre-token-generation trigger can add groups/claims to federated users.

## 4. Lambda triggers you will actually use
| Trigger | Purpose |
|---|---|
| `PreSignUp` | Auto-confirm/auto-verify, block domains, link federated to existing user |
| `PostConfirmation` | Create the app-side profile row |
| `PreTokenGeneration` (V2 for access tokens) | Add custom claims (`tenant_id`, roles), suppress claims |
| `CustomMessage` | Branded verification emails |
| `DefineAuthChallenge`/`Create`/`Verify` | Passwordless / magic-link / custom OTP flows |
Triggers must return in 5 s; keep them small, no cold-start-heavy frameworks.

## 5. Verify the JWT correctly
- JWKS at `https://cognito-idp.<region>.amazonaws.com/<pool-id>/.well-known/jwks.json`;
  cache keys by `kid`.
- Check `iss` = pool URL, `token_use` = `access` (for APIs) or `id` (for identity claims),
  `exp`, and `client_id` (access) / `aud` (ID). The ID token's `aud` is the app client id.
- Use a maintained JWT library (for example `aws-jwt-verify` for Node) rather than hand-rolling.
- **API Gateway**: REST APIs use a Cognito authoriser (ID token or access token with
  `scope` checks); HTTP APIs use a JWT authoriser with `issuer` + `audience`. **ALB** can
  authenticate with the pool and forwards `x-amzn-oidc-data`.
- Authorise on **access token scopes/groups**, not on the ID token, which is for the client.

## 6. Identity pools
- Roles: an *authenticated* and an *unauthenticated* role (guest access optional).
  Trust policy condition `cognito-identity.amazonaws.com:aud = <identity-pool-id>` and
  `:amr contains authenticated`.
- **Role mapping** from user-pool `cognito:groups` or a custom claim selects per-tenant roles;
  use `${cognito-identity.amazonaws.com:sub}` in resource ARNs for per-user S3 prefixes.
- Credentials via `GetId` → `GetCredentialsForIdentity` (enhanced flow; the basic flow has the app
  call STS itself); SDKs/Amplify do this for you.

## Gotchas
- `sub` is the stable user id; email/username can change — key your tables on `sub`.
- Pool regionality: multi-Region replication of a user pool exists as a separate add-on (it
  requires a multi-Region KMS customer managed key); otherwise sign-in is single-Region.
- An app client can have up to two active secrets, which allows secret rotation without a new client.
- `ADMIN_NO_SRP_AUTH`/`ADMIN_USER_PASSWORD_AUTH` need `cognito-idp:AdminInitiateAuth` — never
  grant that to public clients.
- While the account is in the SMS sandbox, only a limited number of verified destination numbers receive SMS; verify the destination or exit the sandbox.
- Feature plans are Lite, Essentials and Plus (new pools default to Essentials); some features (managed login, passkeys, access-token customization, email MFA) need Essentials or Plus. See the Cognito pricing page for cost.

## Verify
- [ ] Public app client has no secret and only SRP + refresh flows enabled.
- [ ] A tampered token (changed payload) is rejected by the API; an expired one returns 401.
- [ ] `PreventUserExistenceErrors` on; sign-in with an unknown user returns the same error as a wrong password.
- [ ] Sign-out revokes the refresh token (reuse fails).
- [ ] Identity pool: a user can only `PutObject` under `private/${sub}/` (test cross-user access is denied).

## Checked

Checked 2026-10-27 against the Amazon Cognito Developer Guide (JWT verification, custom domain, feature plans, identity pool IAM roles and auth flows, multi-Region replication, ALB authentication) and the Cognito quotas page.
- Corrected: refresh token range now 60 minutes to 10 years; user pools now offer multi-Region replication (separate add-on, multi-Region KMS key); an app client can hold two active secrets; SMS goes through the End User Messaging SMS sandbox.
- Confirmed: JWKS URL and `kid` caching, `client_id` (access) versus `aud` (ID), ACM certificate in US East (N. Virginia) for custom domains, identity pool trust-policy keys (`aud`, `amr`), enhanced versus basic flow, ALB `x-amzn-oidc-*` headers, Lite/Essentials/Plus plans with Essentials as default.
- Removed: unconfirmed federated-username pattern, one-hour credential lifetime, named third-party verifier library, and price wording.

Method: documentation only; no commands were run.
