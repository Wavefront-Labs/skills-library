---
id: computing-software.cloud-infrastructure-engineering.google-cloud.iap-with-external-identities
name: iap-with-external-identities
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-aware-proxy, iap-external-identities, identity-platform, customer-identity, multi-tenancy, sign-in-page]
level: practitioner
status: docs-checked
description: "Protect apps with IAP for users outside your Google org via Identity Platform: enable external identities, sign-in page, providers, tenants."
sources: ["https://docs.cloud.google.com/iap/docs/enable-external-identities", "https://docs.cloud.google.com/iap/docs/external-identities", "https://docs.cloud.google.com/iap/docs/create-custom-auth-ui"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAP with external identities

By default IAP uses Google identities and IAM. With **external identities**, IAP uses Identity Platform to
authenticate users from other identity providers, useful when migrating users to Google accounts is impractical.

## Setup
1. Enable and configure Identity Platform (see its Quickstart). Use the **same project** as IAP; different
   projects are not supported.
2. Enable providers: email and password, OAuth (Google, Facebook and others), SAML, OIDC, phone number,
   anonymous. Phone number and anonymous are not supported with multi-tenancy, and passwordless sign-in with an
   email link is not supported with IAP.
3. If you need isolated user pools, turn on multi-tenancy (Getting started with multi-tenancy); otherwise
   configure providers at project level.
4. In the console IAP page, Applications tab, toggle IAP on for the service, then in the side panel click
   **Start** under "Use external identities for authorization".
5. In the Identity Platform panel choose to let IAP create the sign-in page (fastest, no extra service, minor
   customisation via JSON, runs on Cloud Run) or build your own (full control; enter an Authentication URL that
   IAP redirects unauthenticated requests to). Then choose project providers or tenants, tick the ones to
   enable and Save.

If the project is under the domain restricted sharing organization policy constraint, you cannot create public
services by default; use tags and a conditional policy to exempt specific services.

## Tenants
- No tenants: tokens are valid at project level, fine when you do not need isolation.
- One tenant per IAP resource: tokens minted in a tenant context are valid only for that tenant, which stops a
  token for one IAP resource being reused against another in the same project (Google flags the project-level
  reuse as a security risk).
- Multiple tenants per resource: you decide how the user picks one (for example email domain lookup or a list).

## Authorisation
You cannot use IAM for authorisation with external identities. The JSON Web Token IAP generates carries the claims
from the Identity Platform ID token, and the application can filter access on those claims.

## Custom sign-in page
Build with the `gcip-iap` npm module (`npm install gcip-iap --save`), which handles communication between your
app, IAP and Identity Platform. Major versions differ: v1.0.0 needs firebase v9 or later as a peer dependency, and
v2.0.0 needs the modular SDK format, so check the migration notes on the page.

## Switching back
Choose "Use IAM to manage this resource" on the Identity Platform panel. This clears the authentication URL and the
associated project and tenants.

## Verify
- [ ] A partner user signs in via their provider and reaches the app.
- [ ] A user from a tenant that is not enabled is refused.

## Checked
2026-11-09. Confirmed against Enabling external identities, External identities (both read in full) and Create a
custom sign-in page (searched for gcip-iap and versions, not read in full). Removed: the sample JWT claim names
(gcip.firebase.tenant and similar), the claim that Google and external identities cannot share a resource (the
page says only that IAM cannot be used), session-length statement and Identity Platform billing details.
Method: documentation only; no commands were run.
