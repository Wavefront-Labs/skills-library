---
id: computing-software.cloud-infrastructure-engineering.google-cloud.identity-platform-for-customer-identities
name: identity-platform-for-customer-identities
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-platform, gcip, firebase-authentication, ciam, customer-identity, multi-tenancy-auth, oidc-saml-providers, id-token-verification, blocking-functions, mfa-identity-platform, identitytoolkit]
level: practitioner
status: docs-checked
description: "Use Identity Platform for customer sign-in: supported methods, multi-tenancy and limits, blocking functions (events, 7-second limit, claims), and the signing keys endpoint."
sources: ["https://cloud.google.com/identity-platform/docs/concepts-authentication", "https://cloud.google.com/identity-platform/docs/multi-tenancy", "https://cloud.google.com/identity-platform/docs/blocking-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity Platform for customer identities

**Goal:** authenticate your customers (multi-tenant SaaS apps, mobile/web apps, APIs) without writing an auth service, and let your own backends verify the resulting tokens.

## 1. What it provides
- Sign-in with email and password (including password reset emails), phone number (SMS), federated providers (Google, Facebook, Twitter, GitHub; also any SAML or OpenID Connect provider), custom auth system integration (exchange tokens from your server for Identity Platform tokens), and anonymous auth (a temporary account you can later upgrade).
- Built on OAuth 2.0 and OpenID Connect. Federated tokens return to Google's hosted `/__auth/handler` endpoint, so you do not receive or validate the artifact yourself; after sign-in you can use the provided authentication token to verify the user in your own backend.
- Two implementation paths: the client SDK, or the open-source FirebaseUI components (customisable). Enable each sign-in method in the Google Cloud console and complete provider configuration such as the OAuth redirect URL.
- Use the Firebase Admin SDKs when a trusted backend initiates an interaction with Firebase services, to avoid the stricter end-user limits.

## 2. Multi-tenancy
Tenants are silos of users and configuration inside one project (typically B2B). Each tenant has its own identifier, users, identity providers and auth methods, auditing and IAM configuration, quota allocation and usage breakdown.
- Supported in tenants: email/password, social providers (Google, Microsoft, LinkedIn and others), SAML federation, OpenID Connect federation.
- Not supported in tenants: disabling account linking, and a blocking function specific to one tenant. You also cannot disable user signup or user deletion from the console for tenants; use the API.

## 3. Blocking functions
Cloud Run functions that run during registration or sign-in. Available only with Identity Platform (or Firebase Authentication upgraded to it).
- Events: `beforeCreate` (before a new user is saved and before a token is returned) and `beforeSignIn` (after credentials are verified, before the ID token is returned; after the second factor if MFA is used). Creating a user triggers both.
- The function must respond within seven seconds, or the client operation fails. Non-200 responses reach the client.
- Functions apply to all users in the project, including tenants; the user and context tell you the tenant (`context.resource`, for example `projects/project-id/tenants/tenant-id`).
- Linking another identity provider re-triggers `beforeSignIn` (not for email and password). Anonymous and custom authentication do not support blocking functions.
- Block by throwing an `HttpsError` (for example `permission-denied` or `invalid-argument`); the client sees an error that wraps your message.
- Modify instead of block by returning fields: `displayName`, `disabled`, `emailVerified`, `photoURL`, `customClaims`, and `sessionClaims` (`beforeSignIn` only). `customClaims` persist in the database; `sessionClaims` go into the current token only. `beforeSignIn` runs after `beforeCreate` and overwrites fields set in both, except that session claims merge and override same-named custom claims in the token.
- The context includes `ipAddress`, `userAgent`, `locale`, `eventType` (including the sign-in method), `resource`, `credential`. Provider tokens (ID, access, refresh) are passed only for supported providers, and refresh tokens need the Include token credentials option in the console Triggers settings. SAML supplies sign-in claims only.
- Typical uses on the page: allow only an email domain, reject unverified emails, treat a provider's emails as verified, block sign-in from suspicious IPs, record the sign-in IP as a session claim.
- If you delete the Cloud Run function you must also unregister the trigger, or no user can authenticate.

## 4. Verifying tokens in a backend
Use the Firebase Admin SDK `verifyIdToken(idToken, true)`; the second argument also checks whether the token was revoked. The public signing keys are published as a JWK set at `https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com`, whose keys list `RS256`. Identity Platform users are application identities, not IAM principals.

## Gotchas
- A blocking function error is wrapped as an internal error in the client SDK; catch and read the message.
- Test blocking functions against realistic latency: the seven-second budget includes any call to your own services.

## Checked
Confirmed 2026-11-08 against the Authentication, multi-tenancy and blocking-functions pages, and the signing-key JWK endpoint (keys listing RS256). Removed claims the pages do not state: pricing and MAU free tier (pricing page returned 404), 1-hour ID token life, issuer and audience values, custom-claim size limit, MFA types and per-tenant enforcement, Terraform resource names, `identitytoolkit.googleapis.com` activation steps, audit-log advice, and the product comparison table.
Method: docs-only read of cited pages, 2026-11-08
