---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-authentication-profiles-ldap-saml
name: pan-os-authentication-profiles-ldap-saml
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [authentication-profile, pan-os, ldap, radius, saml, server-profile, mfa, kerberos]
level: practitioner
status: draft
description: "Build PAN-OS authentication profiles over LDAP, RADIUS or SAML and test them from the CLI before binding them to admins or GlobalProtect."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/authentication/configure-an-authentication-profile-and-sequence"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: one reusable auth profile consumed by admin login, GlobalProtect, Captive Portal and User-ID.

```
configure
set shared server-profile ldap LDAP-CORP ldap-type active-directory base "DC=example,DC=com" bind-dn "svc-pan@example.com" ssl yes
set shared server-profile ldap LDAP-CORP server dc1 address 192.0.2.20 port 636
set shared authentication-profile AUTH-LDAP method ldap server-profile LDAP-CORP login-attribute sAMAccountName
set shared authentication-profile AUTH-LDAP allow-list [ all ]
commit
```
Set the bind password in the GUI (or let the CLI prompt) so it is not echoed.

Test before use:
```
test authentication authentication-profile AUTH-LDAP username alice password
```
The command prompts for the password. Expect `Authentication succeeded` plus group membership output.

SAML: import the IdP metadata (Device > Server Profiles > SAML Identity Provider), make sure the IdP signing certificate is trusted and that the IdP holds the correct SP entity ID and ACS URL. `test authentication` does not work for SAML; test through a real login.

Gotchas
- An empty `allow-list` means nobody may authenticate.
- Clock skew above a couple of minutes breaks SAML assertions and Kerberos; fix NTP first.
- LDAPS needs the CA that signed the domain controller certificate in the firewall's trusted CA list, otherwise the bind fails with little detail.

## Verify
```
show log system direction equal backward | match authentication
```
Look for success or failure lines naming the profile, and check the `test authentication` output for the group list.
