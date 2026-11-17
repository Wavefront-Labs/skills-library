---
id: computing-software.cybersecurity-defensive.identity-access-management.google-workspace-security
name: google-workspace-security
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [google-workspace-security, google-workspace, 2-step-verification, context-aware-access, advanced-protection-program, scubagoggles, cloud-identity]
level: practitioner
status: docs-checked
description: "Harden Google Workspace identity to the CISA SCuBA baseline: phishing-resistant MFA, super admin limits, app access control, session length and logging."
sources: ["https://github.com/cisagov/ScubaGoggles", "https://github.com/cisagov/ScubaGoggles/blob/main/scubagoggles/baselines/commoncontrols.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Workspace identity hardening

Anchored to the CISA Google Workspace Secure Configuration Baseline for Common Controls (SCuBA),
which the ScubaGoggles tool checks. Policy ids below are the baseline's own (GWS.COMMONCONTROLS.n.m).

## Authentication (group 1)
- 1.1: phishing-resistant MFA is required for all users. Listed methods: FIDO2 security key in
  Google Workspace, phone as security key, FIDO2 key federated from an identity provider, PIV card
  federated from the agency identity provider, and Google passkeys.
- 1.2: if phishing-resistant MFA is not yet enforced, enforce some other MFA method for all users
  (a stopgap).
- 1.3: SMS or voice must not be the MFA method.
- 1.4: set the 2-Step Verification new-user enrolment period to at least one day and at most one week.
- 1.5: disable "Allow users to trust the device".
- 3.1 and 3.2 (should): enable post-SSO verification for users signing in via the organisation's SSO
  profile and via other SSO profiles.

## Passwords and sessions (groups 4, 5)
- 4.1: force re-authentication after an established 12-hour login session expires.
- 5: enforce password strength, length of at least 12 characters (16 recommended), enforcement at next
  sign-in, no reuse, and no password expiry.

## Admins (groups 6, 8, 9)
- 6.1: all administrative accounts are cloud-only, separate from on-premises or federated identity providers.
- 6.2: between two and eight distinct super admin users (break-glass accounts are not counted).
- 8.1 and 8.2: disable account self-recovery for super admins, and for users and non-super admins.
  8.3 (should): disable the ability to add recovery information.
- 9.1: highly privileged accounts are enrolled in the Advanced Protection Program; 9.2 (should): so are
  all sensitive user accounts.
- 17.1 (should): require multi-party approval for sensitive admin actions.

## Access control (groups 2, 10, 11)
- 2.1 (should): implement context-aware access policies based on enterprise device signals. Each rule at a
  given scope is evaluated separately and any rule granting access allows it; a grant at a lower
  level can still apply when a higher-level policy would deny, so test rule interaction. A policy
  requiring company-owned devices needs a list of company-owned device serial numbers.
- 10.1 to 10.5: use application access control to restrict third-party access to all Workspace
  services; do not let users grant consent for low-risk scopes; do not trust unconfigured internal
  applications; do not let users access unconfigured third-party applications; block less secure
  applications.
- 11.1: allow only approved Marketplace applications to be installed.

## Monitoring (groups 13, 14)
- 13.1: enable the required system-defined alerting rules with alerts.
- 14.1: send these logs to the central SIEM: admin audit, enterprise groups audit, login audit, OAuth
  token audit, SAML audit and context-aware access logs.
- 14.2: retain audit logs searchable for at least 3 months and retrievable for at least 12 months.
  The baseline notes that exporting some logs to BigQuery or Cloud log buckets costs extra but can
  meet this.

## Verify
- [ ] Run ScubaGoggles against the tenant and review the HTML and JSON report; it exports settings with
  the Admin SDK API and compares them with the baseline in OPA Rego.
- [ ] 2SV enforcement shows phishing-resistant methods for all users.
- [ ] Super admin count is within the baseline range and Advanced Protection is on for privileged accounts.

## Checked
Method: docs-checked 2026-11-09 against the ScubaGoggles README and the CISA commoncontrols baseline markdown (raw GitHub, read by policy headings; groups 1, 2, 6 and 14 read in full, other groups from their policy statements).
Removed as unconfirmed: the "only security key for admins" and "any except SMS or voice for everyone" setting names, the 2 to 4 super admin figure (baseline says two to eight), the 1-week-for-everyone 2SV claim beyond the baseline's one day to one week range, the 12-24 hour session range (baseline: 12 hours), the edition names for Context-Aware Access, the 6-month console log retention figure, the BigQuery-is-Enterprise-only claim and the retired less-secure-apps remark; the support.google.com sources were not usable as rendered pages.
