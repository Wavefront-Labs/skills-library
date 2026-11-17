---
id: computing-software.systems-network-administration.netbird.sign-in-domains
name: sign-in-domains
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, sign-in-domains, domain-verification, txt-record, cloud-onboarding]
level: practitioner
status: docs-checked
description: "Add and verify NetBird Cloud sign-in domains with a TXT record so users from other email domains join automatically; removal rules and verification statuses."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/team/sign-in-domains.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sign-in domains let users from other email domains join your account automatically. NetBird Cloud only; Owners and Admins manage them.

Add and verify:
1. Settings > Authentication > Sign-in Domains > Add; enter e.g. `company.co.uk`. Status starts Pending.
2. Click Verify. NetBird shows a TXT record to publish at the root of the domain, not `www`.
3. Add it in DNS, click Start Verification. NetBird rechecks and the domain becomes Verified.
4. If never found it shows Unverified; click Verify to restart.

If you cannot change DNS, contact NetBird Support from an address on that domain. A domain can be verified by only one account.

Remove: delete icon on its row. You cannot remove your signup domain or one an SSO integration uses. Removal does not affect users who already joined; it only stops matching new sign-ins.

Verification decides where new users land: add domains before onboarding a team. Users who already have their own account cannot be invited or synced until moved.

## Checked

2026-11-04. Confirmed against the NetBird sign-in domains page: Cloud only, Owner and Admin permissions, add and verify steps, TXT record at the domain root, statuses, support route, one account per domain, removal rules, new-users-only effect. Nothing removed.
Method: documentation only; no commands were run.
