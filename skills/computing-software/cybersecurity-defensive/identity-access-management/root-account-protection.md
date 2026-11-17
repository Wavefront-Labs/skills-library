---
id: computing-software.cybersecurity-defensive.identity-access-management.root-account-protection
name: root-account-protection
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [root-account-protection, aws-root-user, break-glass, centralized-root-access, global-administrator, gcp-super-admin, privileged-access]
level: practitioner
status: draft
description: "Protect cloud root and top-tier accounts: AWS root MFA and centralised root access, no root keys, Azure break-glass Global Admins, GCP super admins, alerting on any use."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-enable-root-access.html", "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access", "https://cloud.google.com/resource-manager/docs/super-admin-best-practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud root account protection

## AWS
- Root user: hardware MFA (FIDO2 - multiple keys can be registered), no access keys (`aws iam get-account-summary` -> `AccountAccessKeysPresent: 0`), unique email on a monitored distribution list, strong password in a vault.
- **Centralised root access** for Organizations member accounts: enable from the management account (`aws iam enable-organizations-root-credentials-management` and `enable-organizations-root-sessions`), then delete member-account root credentials; perform privileged root tasks via short-lived `sts:AssumeRoot` sessions.
- SCP denying root actions in member accounts (`aws:PrincipalArn` like `arn:aws:iam::*:root`).
- Alert: EventBridge rule on `userIdentity.type = Root` in CloudTrail (CIS AWS 1.x / 4.x).

## Azure / Entra
- Two cloud-only emergency access (break-glass) Global Administrator accounts on the `onmicrosoft.com` domain, phishing-resistant auth (FIDO2 keys in safes), excluded from CA policies that could lock out but covered by their own strong policy.
- No other permanent Global Admins; use PIM eligibility.
- Alert on any sign-in by break-glass accounts (Log Analytics alert on SigninLogs UPN).
- Azure subscriptions: "Elevate access" for Global Admin (User Access Administrator at root scope) monitored and removed after use.

## Google Cloud / Workspace
- Super admins: 2-4 dedicated accounts not used daily, security keys enforced, not tied to a single person's mail; org admin roles granted to groups.
- Alert on super admin logins (Workspace audit) and org policy/IAM changes at org level.

## Gotchas
- Root email address on a personal mailbox of a departed employee = account recovery takeover path.
- Break-glass accounts excluded from all CA with no compensating controls are the attacker's favourite target.

## Verify
- [ ] No root access keys anywhere (Org-wide check via IAM credential report or Security Hub control IAM.4).
- [ ] Test alert fires for a break-glass/root sign-in (scheduled quarterly test).
