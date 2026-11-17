---
id: computing-software.systems-network-administration.virtualisation.vcenter-sso-and-identity-sources
name: vcenter-sso-and-identity-sources
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-sso, identity-source, ldaps, active-directory, identity-federation, adfs, entra-id, vsphere-rbac, vmware, vcenter, vsphere]
level: practitioner
status: draft
description: "Connect vCenter SSO to AD over LDAPS or identity federation (ADFS/Entra/Okta), map groups to roles, set password/lockout policy and keep a break-glass account."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-authentication-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vCenter SSO and identity sources

**Goal:** admins log in with directory accounts and MFA, permissions follow AD groups,
and the local SSO admin is only used when the directory is down.

## Choose an identity source
| Option | Notes |
|---|---|
| AD over LDAP(S) | Works everywhere. Use LDAPS (636) with the DC CA chain uploaded; plain LDAP is a finding |
| AD (Integrated Windows Authentication) | Joins VCSA to the domain; deprecated since 7.0 and should not be used for new builds |
| Identity federation (ADFS, Entra ID, Okta, Ping) | vCenter 7/8: browser login redirects to the IdP, enabling MFA and conditional access |
Only **one** federated provider can be configured; the local `vsphere.local` domain always
remains.

## Add AD over LDAPS
1. Administration → Single Sign On → Configuration → Identity Sources → Add → Active
   Directory over LDAP.
2. Base DN for users and groups (narrow it to the admin OU for speed), primary/secondary
   server URLs `ldaps://dc1.<domain>:636`, the DC (or root CA) certificate, and a
   dedicated read-only bind account whose password does not expire unexpectedly.
3. Set as default domain if users should log in without the suffix.

## Map permissions
Grant roles to **AD groups**, never individuals: e.g. `<DOMAIN>\vSphere-Admins` →
Administrator at the vCenter root (propagate), `vSphere-Operators` → a custom role on a
folder. Add the group to `vsphere.local\Administrators` only if they need SSO admin.

## Policies
SSO → Configuration → Local Accounts: password policy and lockout apply to
`vsphere.local` accounts only. Store the `administrator@vsphere.local` password in the
vault, test it quarterly, and alert on its use (it appears in VCSA logs and events).

## Gotchas
- Expired DC certificates break LDAPS logins for everyone; track their expiry and upload
  the new chain before rollover.
- Bind account lockout (password change elsewhere) also breaks every login.
- Nested group membership resolves, but deep nesting slows login.
- Federation: the redirect URI and certificate must be updated on the IdP if the VCSA
  FQDN or machine certificate changes.

## Verify
Log in as a test AD user in each mapped group and confirm the expected privileges;
`administrator@vsphere.local` still logs in; Identity Sources page shows the certificate
expiry date.
