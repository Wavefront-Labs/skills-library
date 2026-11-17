---
id: computing-software.systems-network-administration.virtualisation.vcenter-sso-password-and-lockout-policy
name: vcenter-sso-password-and-lockout-policy
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [sso-password-policy, sso-lockout-policy, vcenter-sso, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Set vCenter SSO password, lockout and token policies for vsphere.local accounts, and stop the administrator account from expiring unexpectedly."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-vcenter-server-systems/vcenter-server-password-requirements-and-lockout-behavior.html
  - https://knowledge.broadcom.com/external/article?legacyId=2146224
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SSO password and lockout policies

**Goal:** vsphere.local accounts follow security policy without surprise lockouts or expired administrator passwords.

## Where
vSphere Client -> Administration -> Single Sign On -> **Configuration** -> *Local Accounts*. These policies apply only to the SSO domain (vsphere.local); AD/LDAP accounts follow their directory's policy.

## Password policy (defaults)
The `administrator@vsphere.local` password by default must be at least 8 characters, at
most 20, and contain at least one lowercase, one numeric and one special character
(non-ASCII allowed). Administrators can change the policy; see the vSphere Authentication
documentation.

## Lockout policy (defaults)
Maximum failed attempts: 5 consecutive attempts within 3 minutes; a locked account unlocks automatically after 5 minutes. A service account with a stale password in a script or backup tool locks itself repeatedly; find it in the SSO logs on the VCSA. The default SSO domain administrator account is not affected by the lockout policy (only by the password policy).

## Token policy
Clock tolerance, maximum token lifetime and renewal counts are configurable. Clock skew between vCenter and clients or other nodes beyond tolerance causes login failures; fix NTP first.

## Stop administrator expiry
Password expiry of `administrator@vsphere.local` causes outages for integrations. Either rotate on a schedule with a calendar reminder, or check the `dir-cli user modify` options for a non-expiring account in the vSphere Authentication documentation.
Service accounts for integrations should be dedicated SSO users (or AD accounts) with least-privilege roles, not the administrator.

## Unlock or reset
`dir-cli password change` (known password) and `dir-cli password reset` (a vCenter Single Sign-On administrator resets a forgotten password) run from the VCSA shell; a locked non-administrator account unlocks automatically after the unlock time.

## Verify
Configuration page shows the new values; a test user locks after the configured number of bad logins and unlocks after the unlock time.

## Checked
2026-10-31: Lockout defaults (5 consecutive failed attempts within 3 minutes, automatic unlock after 5 minutes), the administrator password requirements (8-20 characters, at least one lowercase/numeric/special), `dir-cli password change`/`dir-cli password reset`, and the fact that the SSO domain administrator is not affected by the lockout policy were confirmed on the vCenter Password Requirements and Lockout Behavior page. Removed unconfirmed figures: 90-day lifetime, previous-5 reuse, 600 s clock tolerance, character-class detail beyond the confirmed list, SSO log file names and dir-cli flag details.
Method: documentation only; no commands were run.
