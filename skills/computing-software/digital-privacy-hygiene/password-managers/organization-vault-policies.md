---
id: computing-software.digital-privacy-hygiene.password-managers.organization-vault-policies
name: organization-vault-policies
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, organization-policies, family-vault, password-manager-cli]
level: practitioner
status: draft
description: "Enforce organisation policies in Bitwarden or 1Password teams: required 2FA, master password strength, single organisation, vault timeout and data ownership."
sources:
  - "https://bitwarden.com/help/policies/"
  - "https://support.1password.com/business-security-practices/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Organisation vault policies

**Goal:** for a small business or club vault, set the guardrails once so every member meets a baseline.

## Bitwarden policies (Teams/Enterprise, check plan)
Admin Console > Settings > Policies:
| Policy | Set to |
|---|---|
| Require two-step login | On (members without 2FA are removed/blocked) |
| Master password requirements | Min complexity score and length 14+ |
| Password generator | Minimum length/types for generated passwords |
| Single organisation | Stops members joining other orgs (Enterprise) |
| Enforce organisation data ownership | Removes personal vault for org users (Enterprise; work data stays with the org) |
| Vault timeout | Max timeout, action Lock or Log out |
| Account recovery administration | Lets admins reset members' master passwords after enrolment |
| Send options | Restrict or disable Send |

## 1Password Business
Admin console > Policies: account password policy, sign-in attempt lockout, require two-factor authentication,
firewall rules (allowed countries/IPs), app usage rules.

## Rollout
1. Announce the date; give members time to enable 2FA.
2. Enable policies one at a time; watch for locked-out members.
3. Document the recovery route (account recovery admin, or 1Password admin recovery).

## Gotchas
- Turning on "Require two-step login" removes non-compliant members in Bitwarden; warn first.
- Account recovery needs member enrolment; enabling it later doesn't cover existing members until they enrol.
