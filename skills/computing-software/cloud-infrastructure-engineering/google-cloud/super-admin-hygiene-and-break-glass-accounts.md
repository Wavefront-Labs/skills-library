---
id: computing-software.cloud-infrastructure-engineering.google-cloud.super-admin-hygiene-and-break-glass-accounts
name: super-admin-hygiene-and-break-glass-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, super-admin, break-glass, cloud-identity, 2sv, security-keys, account-recovery, super-admin-recovery, admin-account-hygiene, break-glass-account]
level: advanced
status: docs-checked
description: "Run Cloud Identity super-admins safely: dedicated accounts, security keys, recovery options, a sealed break-glass account, and separation from organisation admin."
sources: ["https://cloud.google.com/resource-manager/docs/super-admin-best-practices", "https://support.google.com/a/answer/9011373", "https://cloud.google.com/architecture/security-foundations/authentication-authorization", "https://support.google.com/a/answer/33561"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Super-admin hygiene and break-glass accounts

**Goal:** the accounts that can take over the whole organisation are few, phishing-resistant,
recoverable, and never used for day-to-day work.

## 1. Rules (from Google's guidance)
1. **More than one super admin**, each managed by a separate individual; never share an admin account.
2. **Dedicated super-admin accounts**, separate from the daily account (`alice@example.com` and `alice-admin@example.com`).
3. **Enforce 2-Step Verification with security keys**; enrol more than one security key per admin and keep spares in a safe place. Backup codes: print and store securely.
4. **Keep super admins out of the cloud admin group.** Put Organization Administrators in a private Google Cloud admin group, grant that group `roles/resourcemanager.organizationAdmin` (or a subset), and leave the super admin out of it.
5. Use limited admin roles for daily administration; sign in as super admin only for specific tasks and sign out.
6. **Recovery options**: add a recovery phone and email to admin accounts. Self-recovery of super admin passwords is off by default for new customers; keep it off and make sure Organization Administrators know the super-admin recovery process.
7. **Alerts**: set up admin email alerts (suspicious sign-in, changes by another admin) and review Admin log events (super admin activity shows as `_SEED_ADMIN_ROLE`). In Cloud Monitoring, alert on `SetIamPolicy()` calls.
8. With a third-party identity source, apply the same suspension policy to Cloud Identity and the source.
9. A short sign-in period for super admins is possible on Workspace Enterprise/Business or Cloud Identity Premium.
10. The Advanced Protection Program can be enrolled for super admin accounts.

## 2. Break-glass account
Keep one extra super admin account for emergencies (for example `breakglass@example.com`): long random
password held under dual control, security key in a safe, excluded from third-party SSO so an IdP outage
cannot lock you out, every use treated as an incident, and alerts on any login to it. These are practice
recommendations, not Google requirements.

## 3. Quarterly checks
- Admin roles report: no leavers, no service accounts or shared mailboxes with super admin.
- `organizationAdmin` at org level held by groups only; membership reviewed.
- Automation that suspends leavers excludes admin accounts only if you decide so deliberately.

## Verify
- [ ] More than one named dedicated super admin plus the break-glass account.
- [ ] Security-key 2SV enforced and spare keys enrolled.
- [ ] Break-glass login tested with SSO bypassed, and the alert fired.

## Checked
2026-10-28. Confirmed on the Resource Manager super-admin best-practices page and the Google Workspace admin best
practices page: multiple separate super admins, separate admin accounts, security keys and spares, backup codes,
admin group separation, sign-out advice, recovery options and default self-recovery, admin email alerts, Admin log
`_SEED_ADMIN_ROLE`, SetIamPolicy alerting, short sign-in period availability, Advanced Protection. Removed: the "2-3"
count, 8-hour session, Admin console menu paths, "recovery takes days", and claims about context-aware access, deny
policies and what super admins can do.
Method: documentation only; no commands were run.
