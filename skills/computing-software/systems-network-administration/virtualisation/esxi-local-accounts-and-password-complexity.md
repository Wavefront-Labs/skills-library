---
id: computing-software.systems-network-administration.virtualisation.esxi-local-accounts-and-password-complexity
name: esxi-local-accounts-and-password-complexity
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-local-accounts, passwdqc, esxi-hardening, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Create and manage local ESXi users and roles, set passwdqc password complexity, history and lockout settings, and keep vpxuser and DCUI access safe."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/esx-upgrade/upgrading-esxi-hosts-upgrade/esxi-requirements-upgrade/esxi-passwords-and-lockout-upgrade.html
  - https://knowledge.broadcom.com/external/article/412881/esxi-password-policy-account-lockout-be.html
  - https://raw.githubusercontent.com/openwall/passwdqc/master/README
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Local ESXi accounts and password complexity

**Goal:** a minimal set of named local accounts with a policy-compliant password rule set.

## Accounts
```bash
esxcli system account add -i opsadmin -p '<pwd>' -c '<pwd>' -d 'Ops break-glass'
esxcli system permission set -i opsadmin -r Admin        # Admin | ReadOnly | NoAccess
esxcli system account list
esxcli system permission list
```
- Never delete or change `vpxuser` (vCenter manages it) or `dcui`.
- Keep `root` with a vaulted password; add named admin accounts for audit.
- In lockdown mode, *Exception Users* keep their permissions.

## Password complexity: `Security.PasswordQualityControl`
Default: `retry=3 min=disabled,disabled,disabled,7,7`. The five `min` values are minimum lengths for passwords using 1, 2 character classes, passphrases, 3 classes, and 4 classes. `disabled` forbids that class count.
```bash
esxcli system settings advanced set -o /Security/PasswordQualityControl -s 'retry=3 min=disabled,disabled,disabled,disabled,15'
```
Notes: an uppercase first character or a digit as the last character does not count towards a class; `passphrase=0` disables passphrases.

## History, expiry and lockout
| Advanced setting | Default | Typical hardened |
|---|---|---|
| `Security.PasswordHistory` | 0 | 5 |
| `Security.PasswordMaxDays` | see ESXi Passwords and Account Lockout | 90 for named users |
| `Security.AccountLockFailures` | 5 | 5 (0 disables) |
| `Security.AccountUnlockTime` | see ESXi Passwords and Account Lockout | 900 s |

A locked user unlocks after `AccountUnlockTime`; see the ESXi Passwords and Account
Lockout page for early-unlock options.

## Fleet consistency
Apply with host profiles or your automation tool of choice; AD join is better for named
admins at scale.

## Verify
`esxcli system settings advanced list -o /Security/PasswordQualityControl` shows the rule; setting a weak password is rejected with a quality error.

## Checked
2026-10-31: The `Security.PasswordQualityControl` default (`retry=3 min=disabled,disabled,disabled,7,7`), the five `min` slots, the leading-uppercase/trailing-digit class rule, `Security.PasswordHistory`, `Security.AccountLockFailures`, `Security.AccountUnlockTime` and `esxcli system account add/permission` confirmed on the ESXi Passwords and Account Lockout page and KB 412881; the `min=` semantics and `passphrase=0` behaviour confirmed in the passwdqc README. Removed unconfirmed figures: the exact 99999/900 s default values, `DCUI.Access`, the `esxcli system account set` unlock command and the PowerCLI cmdlet example.
Method: documentation only; no commands were run.
