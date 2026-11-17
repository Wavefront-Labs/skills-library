---
id: computing-software.cloud-infrastructure-engineering.azure.multi-tenant-apps-and-publisher-verification
name: multi-tenant-apps-and-publisher-verification
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-registrations, multi-tenant-app, publisher-verification, admin-consent, issuer-validation, saas]
level: advanced
status: docs-checked
description: "Build a multi-tenant Entra app: sign-in audience, /organizations authority, per-tenant issuer validation, admin consent onboarding and publisher verification."
sources: ["https://learn.microsoft.com/entra/identity-platform/howto-convert-app-to-be-multi-tenant", "https://learn.microsoft.com/entra/identity-platform/publisher-verification-overview", "https://learn.microsoft.com/entra/identity-platform/v2-admin-consent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-tenant apps and publisher verification

**Goal:** a SaaS app customers can onboard from their own tenants safely, with a verified publisher badge.

## Registration
- Supported account types: *Accounts in any organizational directory* (`signInAudience: AzureADMultipleOrgs`),
  or plus personal accounts (`AzureADandPersonalMicrosoftAccount`).
- Authority: `https://login.microsoftonline.com/organizations` (work/school) or `/common`.
- The app registration lives in your tenant; each customer gets a **service principal** (enterprise app) in theirs
  when consent happens.

## Onboarding (admin consent)
Send the customer admin to:
```
https://login.microsoftonline.com/<customer-tenant-or-organizations>/v2.0/adminconsent?client_id=<appId>&scope=https://graph.microsoft.com/.default&redirect_uri=<uri>&state=<nonce>
```
The redirect returns `tenant` and `admin_consent=True`; record the tenant ID as an onboarded customer.

## Token validation
- Don't accept any issuer: validate `tid` (and issuer `https://login.microsoftonline.com/{tid}/v2.0`) against your
  list of onboarded tenants.
- Key data by `tid` + `oid`, never by email or UPN.

## Publisher verification
- Verification uses a Microsoft AI Cloud Partner Program ID; see the publisher verification overview for the current requirements and steps.
- Effect: a verified publisher shows on consent prompts; unverified publishers get a warning on the consent screen.

## Gotchas
- Ask for the least Graph permission you need (high-privilege ones such as `Directory.ReadWrite.All` normally need admin consent) and use incremental consent.
- Customers can disable your app or require assignment in their tenant - handle the resulting sign-in errors.

## Verify
- [ ] A test customer tenant can onboard via admin consent; tokens from an un-onboarded tenant are rejected by your API.

## Checked
2026-10-28. Confirmed on the Learn multi-tenant, publisher verification and admin consent pages: /organizations and /common authorities, issuer validation against the token iss, `admin_consent=True` in the redirect, verified publisher and unverified warning. Removed: partner-account domain rules, app instance property lock, named AADSTS codes, the claim about user consent under the default policy.
Method: documentation only; no commands were run.
