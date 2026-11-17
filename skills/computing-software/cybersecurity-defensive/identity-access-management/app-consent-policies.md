---
id: computing-software.cybersecurity-defensive.identity-access-management.app-consent-policies
name: app-consent-policies
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [entra-id, app-consent-policy, oauth-consent, illicit-consent-grant, admin-consent-workflow, enterprise-applications]
level: practitioner
status: docs-checked
description: "Lock down OAuth app consent in Entra ID: user consent settings, admin consent workflow, permission classifications, reviewing existing grants and detecting illicit consent."
sources: ["https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-user-consent", "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-admin-consent-workflow", "https://learn.microsoft.com/en-us/defender-office-365/detect-and-remediate-illicit-consent-grants"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App consent policies

**Goal:** users cannot grant malicious or over-privileged OAuth apps access to mail and
files (illicit consent grant phishing), while legitimate app requests still get a quick path.

## User consent setting
Entra ID > Enterprise applications > Consent and permissions > User consent settings:
- **Do not allow user consent** (strictest), or
- **Allow user consent for apps from verified publishers, for selected permissions** (limited
  consent): only for permissions you classify as low impact, for apps from verified publishers or registered in your tenant.

## Permission classifications
Classify only low-impact delegated permissions (basic sign-in and profile scopes) as consentable by users.
Anything touching mail, files, or other users should require admin consent.

## Admin consent workflow
Enable it so users can request apps they cannot consent to; designate reviewers (identity or
security team); set expiry and notification. Reviewers check: publisher verification,
permissions requested vs need, application vs delegated permissions (application permissions
can reach data across the tenant), reply URLs, vendor reputation.

## Review existing grants
- Entra > Enterprise applications: filter user-consented apps, or list delegated permission grants through Microsoft Graph.
- Look for high-risk scopes (broad mail, file, mailbox-settings or full-access scopes), unverified publishers, apps with few users and broad scopes,
  names mimicking Microsoft.
- Revoke unneeded grants and disable/delete malicious service principals.

## Detect
- Audit log "Consent to application" events with risky scopes;
  alert when a user consents shortly after a phishing click.
- Response: revoke the grant, remove the service principal, revoke user sessions, review
  mailbox rules and data accessed via the app's sign-in logs (service principal sign-ins).

## Gotchas
- Removing user consent without a working admin-consent workflow drives users to shadow IT.
- Multi-tenant apps from attackers can be "verified" too; verification is a signal, not proof.
- Existing grants persist after you tighten settings; review them.

## Verify
A test user cannot consent to an app requesting mail access; the request lands in the admin
workflow; the quarterly grant review shows no unexplained high-risk user consents.

## Checked

2026-10-28. Confirmed against the user consent configuration page and the illicit consent grant page: options to disable user consent or allow limited consent for verified publishers and permissions classified low impact, admin consent workflow, Consent to application audit activity. Removed: named Graph scopes, group owner consent bullet, the Get-MgOauth2PermissionGrant example, 'Microsoft recommended baseline' wording, Defender for Cloud Apps bullet.

Method: documentation only; no commands were run.
