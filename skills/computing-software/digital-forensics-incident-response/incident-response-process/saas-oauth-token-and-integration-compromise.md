---
id: computing-software.digital-forensics-incident-response.incident-response-process.saas-oauth-token-and-integration-compromise
name: saas-oauth-token-and-integration-compromise
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [oauth-token-theft, oauth-consent-grant, saas-forensics, cloud-incident-response, dfir]
level: advanced
status: docs-checked
description: "Investigate stolen OAuth tokens and compromised SaaS integrations: why tokens bypass user login, inventorying integrations, GitHub organisation audit log searches, containment."
sources: ["https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization", "https://datatracker.ietf.org/doc/html/rfc6749"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SaaS OAuth token and integration compromise

**Goal:** third-party integrations hold OAuth tokens. If the integration vendor or a token store is breached, an attacker can use those tokens against your SaaS tenants without a user signing in.

## How tokens behave (RFC 6749)
- Access tokens are credentials used to access protected resources; they represent specific scopes and durations of access granted by the resource owner.
- Refresh tokens are credentials used to obtain new access tokens when the current one expires or is invalid, or to obtain tokens of identical or narrower scope. Issuing one is optional for the authorization server.
- So a stolen refresh token can keep minting access tokens, and use of a token does not involve the user's password or MFA prompt (inference from the above; confirm for each platform). Revoking means invalidating at the authorisation server or removing the integration, not only changing a user password.

## Inventory
List the authorised apps, integrations and tokens per platform, with scopes and who approved them, and note which are vendor-hosted (token stored at the vendor), since those are in scope when the vendor is breached.

## Hunt: GitHub organisation audit log
Per GitHub's page:
- Owners only; the web audit log lists events from the last 180 days (the last three months shown by default; give a date range with `created` to see older ones).
- Entries are named category.operation (for example `repo.create`). Relevant categories include `oauth_application`, `integration_installation`, `integration_installation_request`, `personal_access_token` and `repo`.
- Search with qualifiers: `action:`, `actor:`, `operation:` (access, authentication, create, modify, remove, restore, transfer), `repo:` (include the account name), `created:` (ISO 8601, with `>=`, `<=` and `..` ranges) and `country:`. Text search is not supported.
- Export as JSON or CSV after filtering; exports have a hard limit of 100 MB compressed or 10 minutes, so narrow first. Exported keys include `action`, `actor`, `actor_location.country_code`, `repo` and `created_at`.
- The audit log API is for organisations on GitHub Enterprise Cloud, so export early for others given the 180 day window.

For Salesforce, Slack and Google Workspace, use each vendor's own audit documentation; their pages were not readable here and no log or event names are given.

## Contain
Revoke the tokens or uninstall the integration, and rotate secrets that were visible in data the integration could read (repositories and records often hold credentials). Where the platform supports it, restrict tokens by network allow-list (check platform documentation).

## Downstream scoping
Secrets found in accessed repositories are treated as leaked keys; exported customer data goes to the breach-notification assessment.

## Verify
All tokens for the compromised integration are revoked and no API activity under its client follows.

## Checked
Dated 2026-11-08. Confirmed against GitHub "Reviewing the audit log for your organization" (180 days, owners only, categories, qualifiers, export limits and keys, Enterprise Cloud API) and RFC 6749 sections 1.4 and 1.5. Removed: the Salesforce page (stub, unreadable), all Salesforce, Slack and Google event names, GitHub event names not on the page (oauth_access.create, git.clone, repo.download_zip), the actor_ip and programmatic_access_type API fields, and the Salesforce Shield claim.
Method: docs-only read of cited pages, 2026-11-08
