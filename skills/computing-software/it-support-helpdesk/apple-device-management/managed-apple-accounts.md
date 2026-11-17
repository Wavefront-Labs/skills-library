---
id: computing-software.it-support-helpdesk.apple-device-management.managed-apple-accounts
name: managed-apple-accounts
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, abm-accounts, managed-apple-accounts, managed-apple-id, accounts]
level: practitioner
status: docs-checked
description: "Create Managed Apple Accounts in Apple Business or School Manager, choose the creation method, and know which Apple services these accounts can and cannot use."
sources:
  - "https://support.apple.com/guide/deployment/about-managed-apple-accounts-depdc4ba8d82/web"
  - "https://support.apple.com/guide/business/manually-add-users-axme2e2158c6/web"
  - "https://support.apple.com/guide/business/service-access-with-managed-apple-accounts-axm171b3ee95/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# managed-apple-accounts

Goal: provide organisation-owned Apple accounts for User Enrolment, Shared iPad and work data in iCloud.
- Creation methods: manually in the web portal; federated authentication with Google Workspace, Microsoft Entra ID or another identity provider; directory sync using OpenID Connect or SCIM. Student information system and SFTP CSV import are Apple School Manager only.
- Manual creation in Apple Business: People > Users, then Add. Until the user signs in and changes their password the account is not active.
- Roles come from the account roles table on the "About Managed Apple Accounts" page; the page and the Apple Business guide give different Administrator limits, so check the current number in the portal rather than relying on a figure here.
- Services: Managed Apple Accounts cannot make purchases in the stores (apps are distributed by the organisation through Managed Distribution), and Shared iPad works only with Managed Apple Accounts. iMessage, FaceTime and collaboration are on by default and Calendar is off by default; Find My, iCloud Family Sharing and iCloud Mail are not available.
Practice: decide the creation method first (federation or sync scales; manual suits small pilots), then enrol the pilot group before the whole domain.
Gotcha: an account that was created but never signed into stays inactive, so do not count it as a working login.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "About Managed Apple Accounts"; Apple Business User Guide "Manually add users" and "Service access with Managed Apple Accounts". Also read "Change a user's domain information" and "Transfer Apple services" in the Apple Business guide, which did not confirm the claim-notice time limit.
- Removed as unconfirmed: "Accounts > Add Account", "Preferences > Sign in and Sync / Access", bulk CSV import in Apple Business Manager, the account-transfer claim notice time limit, the Active and Pending status labels and the Verify steps.
- The original sources were the guides' welcome pages and were replaced with the specific pages above.
